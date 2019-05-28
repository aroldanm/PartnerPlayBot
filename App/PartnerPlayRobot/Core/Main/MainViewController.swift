//
//  MainViewController.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 25/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation
import UIKit

protocol MainViewControllerProtocol {
    var begin: (()->())? { get set }
    var disconnect: (()->())? { get set }

    func loadCompleted()
    func showErrorConnection()
    func changeStatus(to status: ConnectionStatus)
}

class MainViewController: UIViewController {
    @IBOutlet weak var beginButton: UIButton!
    @IBOutlet weak var disconnectButton: UIButton!
    @IBOutlet weak var titleLabel: UILabel!
    @IBOutlet weak var welcomeLabel: UILabel!
    @IBOutlet weak var labelHeightConstraint: NSLayoutConstraint!
    @IBOutlet weak var loadingIndicator: UIActivityIndicatorView!

    private let presenter = MainPresenter()
    
    var disconnect: (() -> ())?
    var begin: (()->())?

    override func viewDidLoad() {
        super.viewDidLoad()
        setup()
        setupView()
        loadResource()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        presenter.setupDelegates()
        changeStatus(to: presenter.connectionStatus)
    }
}

extension MainViewController: MainViewControllerProtocol {
    func loadCompleted() {
        hideLoading()
        beginButton.isEnabled = true
        if beginButton.isHidden {
            showBeginButton()
        } else {
            beginButton.alpha = 1
        }
    }

    func showErrorConnection() {
        hideLoading()
        let alert = UIAlertController(title: NSLocalizedString("error_not_connection_title",
                                                               comment: "Error"),
                                      message: NSLocalizedString("error_not_connection_message", comment: "message"),
                                      preferredStyle: .alert)
        if beginButton.isHidden {
            alert.addAction(UIAlertAction(title: NSLocalizedString("try_again", comment: "Try again"),
                                          style: .default, handler: { _ in
                                            self.loadResource()
            }))
        } else {
            alert.addAction(UIAlertAction(title: NSLocalizedString("understood", comment: "Understood"),
                                          style: .default, handler: nil))
        }
        self.present(alert, animated: true, completion: nil)
    }

    func changeStatus(to status: ConnectionStatus) {
        switch status {
        case .connected:
            disconnectButton.isHidden = false
            UIView.animate(withDuration: 0.25) {
                self.disconnectButton.alpha = 1
                self.beginButton.backgroundColor = self.presenter.beginButtonProperties.background
                self.beginButton.setTitle(self.presenter.beginButtonProperties.title, for: .normal)
            }
        case .disconnected,
             .failure:
            disconnectButton.isHidden = true
            UIView.animate(withDuration: 0.25) {
                self.disconnectButton.alpha = 0
                self.beginButton.backgroundColor = self.presenter.connectButtonProperties.background
                self.beginButton.setTitle(self.presenter.connectButtonProperties.title, for: .normal)
            }
        }
        
    }
}

private extension MainViewController {
    func setup() {
        presenter.viewController = self
        presenter.setupView()
    }

    func setupView() {
        view.backgroundColor = presenter.backgroundColor
        //Button
        beginButton.backgroundColor = presenter.beginButtonProperties.background
        beginButton.setTitleColor(presenter.beginButtonProperties.titleColor, for: .normal)
        beginButton.setTitle(presenter.beginButtonProperties.title, for: .normal)
        beginButton.layer.cornerRadius = 5
        beginButton.isHidden = true
        beginButton.alpha = 0
        
        let image = UIImage(named: "ic_disconnect")?.withRenderingMode(.alwaysTemplate)
        disconnectButton.setImage(image, for: .normal)
        disconnectButton.tintColor = presenter.disconnectButtonProperties.tintColor
        disconnectButton.isHidden = true
        disconnectButton.alpha = 0
        
        //Label
        titleLabel.textColor = presenter.titleProperties.textColor
        titleLabel.text = presenter.titleProperties.text
        
        welcomeLabel.textColor = presenter.welcomeProperties.textColor
        welcomeLabel.text = presenter.welcomeProperties.text
        welcomeLabel.isHidden = true
        welcomeLabel.alpha = 0

        //Indicator
        loadingIndicator.color = .white
        loadingIndicator.isHidden = true
        loadingIndicator.alpha = 0
        loadingIndicator.hidesWhenStopped = true
        loadingIndicator.startAnimating()
    }
    
    func loadResource() {
        beginHudAnimation {
            self.presenter.loadResources()
        }
    }
    
    func beginHudAnimation(completion: @escaping () -> ()) {
        self.loadingIndicator.isHidden = false
        UIView.animate(withDuration: 0.25, animations: {
            self.loadingIndicator.alpha = 1
            self.loadingIndicator.startAnimating()
        }) { _ in
            if self.beginButton.alpha == 1 {
                self.beginButton.isEnabled = false
                self.beginButton.alpha = 0.5
            }
            completion()
        }
    }

    func hideLoading() {
        loadingIndicator.stopAnimating()
    }

    func showBeginButton() {
        self.beginButton.isHidden = false
        self.welcomeLabel.isHidden = false
        self.disconnectButton.isHidden = false
        labelHeightConstraint.constant = -(titleLabel.frame.size.height+25)
        UIView.animate(withDuration: 0.7) {
            self.view.layoutIfNeeded()
            self.welcomeLabel.alpha = 1
            self.disconnectButton.alpha = 1
            self.titleLabel.transform = CGAffineTransform(scaleX: 1.5, y: 1.5)
        }
        
        UIView.animate(withDuration: 0.5, delay: 0.2, options: .beginFromCurrentState, animations: {
            self.beginButton.alpha = 1
        }, completion: nil)
    }
}

private extension MainViewController {
    @IBAction func beginButton(_ sender: Any) {
        if case ConnectionStatus.connected = presenter.connectionStatus {
            begin?()
        } else {
            beginHudAnimation {
                self.begin?()
            }
        }
    }

    @IBAction func disconnectButton(_ sender: Any) {
        disconnect?()
    }
}

