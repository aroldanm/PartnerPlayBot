//
//  MainViewController.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 25/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation
import UIKit

protocol MainViewController {
    var begin: (()->())? { get set }
}

class MainViewControllerImpl: UIViewController {
    @IBOutlet weak var beginButton: UIButton!
    @IBOutlet weak var titleLabel: UILabel!
    @IBOutlet weak var welcomeLabel: UILabel!
    @IBOutlet weak var labelHeightConstraint: NSLayoutConstraint!

    private let businessLogic = MainBusinessLogic()
    
    var begin: (()->())?

    override func viewDidLoad() {
        super.viewDidLoad()
        setup()
        setupView()
        DispatchQueue.main.asyncAfter(deadline: .now()+1.5) {
            self.beginAnimate()
        }
    }
}

extension MainViewControllerImpl: MainViewController {
}

private extension MainViewControllerImpl {
    func setup() {
        businessLogic.viewController = self
        businessLogic.setup()
    }

    func setupView() {
        view.backgroundColor = businessLogic.backgroundColor
        //Button
        beginButton.backgroundColor = businessLogic.buttonProperties.background
        beginButton.setTitleColor(businessLogic.buttonProperties.titleColor, for: .normal)
        beginButton.setTitle(businessLogic.buttonProperties.title, for: .normal)
        beginButton.layer.cornerRadius = 5
        beginButton.alpha = 0
        
        //Label
        titleLabel.textColor = businessLogic.titleProperties.textColor
        titleLabel.text = businessLogic.titleProperties.text
        
        welcomeLabel.textColor = businessLogic.welcomeProperties.textColor
        welcomeLabel.text = businessLogic.welcomeProperties.text
        welcomeLabel.alpha = 0
        
    }
    
    func beginAnimate() {
        labelHeightConstraint.constant = -(titleLabel.frame.size.height+25)
        UIView.animate(withDuration: 0.7) {
            self.view.layoutIfNeeded()
            self.beginButton.alpha = 1
            self.welcomeLabel.alpha = 1
            self.titleLabel.transform = CGAffineTransform(scaleX: 1.5, y: 1.5)
        }
    }
}

private extension MainViewControllerImpl {
    @IBAction func beginButton(_ sender: Any) {
        begin?()
    }
}

