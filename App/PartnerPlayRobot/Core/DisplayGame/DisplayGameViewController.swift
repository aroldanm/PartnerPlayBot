//
//  DisplayGameViewController.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 27/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import UIKit
import AudioToolbox
import AVFoundation

enum DisplayGameAlertResponse {
    case done
    case cancel
}

protocol DisplayGameViewControllerProtocol {
    func showAlert(title: String, message: String, done: String, cancel: String?, response: @escaping (DisplayGameAlertResponse) -> ())
    func addLog(_ text: String)
    func setTurn(turn: Turn)
    func clearActions()
    func addLabelAction(message: String)
    func addGifAction(image: UIImage)
}

class DisplayGameViewController: UIViewController {
    @IBOutlet weak var closeButton: UIButton!
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var terminal: UITextView!
    @IBOutlet weak var turnImage: UIImageView!
    @IBOutlet weak var turnLabel: UILabel!
    @IBOutlet weak var stackView: UIStackView!

    let presenter = DisplayGamePresenter()
    let time_animation: Double = 0.25

    override func viewDidLoad() {
        super.viewDidLoad()
        setupView()
        setup()
    }
}

private extension DisplayGameViewController {
    func setup() {
        presenter.viewController = self
        presenter.setup()
    }

    func setupView() {
        view.backgroundColor = presenter.backgroundColor
        
        terminal.text = ""
        
        //Button
        let image = UIImage(named: "ic_close")?.withRenderingMode(.alwaysTemplate)
        closeButton.setImage(image, for: .normal)
        closeButton.tintColor = presenter.buttonCloseProperties.tintColor
        
        //ImageView
        imageView.contentMode = .scaleAspectFill
        imageView.clipsToBounds = true
        imageView.layer.cornerRadius = 5
        imageView.layer.borderWidth = 3
        imageView.transform = CGAffineTransform(scaleX: -1, y: 1)
        
        //Turn label and image
        turnLabel.isHidden = true
        turnImage.isHidden = true
        
        //StackView
        stackView.layoutMargins = UIEdgeInsets(top: 0, left: 0, bottom: 0, right: 0)
        stackView.isLayoutMarginsRelativeArrangement = true
    }
    
    func speak(message: String) {
        let utterance = AVSpeechUtterance(string: message)
        utterance.voice = AVSpeechSynthesisVoice(language: "es-MX")
        let synthesizer = AVSpeechSynthesizer()
        synthesizer.speak(utterance)
    }

    @IBAction func closeView(_ sender: Any) {
        presenter.dismiss()
    }
}

extension DisplayGameViewController: DisplayGameViewControllerProtocol {
    func clearActions() {
        DispatchQueue.main.async {
            self.stackView.arrangedSubviews.forEach { item in
                self.stackView.removeArrangedSubview(item)
                item.removeFromSuperview()
            }
        }
    }
    
    func addLabelAction(message: String) {
        DispatchQueue.main.async {
            let label = UILabel(frame: CGRect(x: 0, y: 0,
                                              width: self.stackView.frame.size.width-20,
                                              height: 0))
            label.textColor = .white
            label.font = UIFont.boldSystemFont(ofSize: 36)
            label.textAlignment = .center
            label.numberOfLines = 0
            label.adjustsFontSizeToFitWidth = true
            label.text = message
            label.sizeToFit()
            
            self.stackView.addArrangedSubview(label)
            
            label.translatesAutoresizingMaskIntoConstraints = false
            label.heightAnchor.constraint(equalToConstant: label.frame.size.height).isActive = true
            
            self.speak(message: message)
        }
    }
    
    func addGifAction(image: UIImage) {
        DispatchQueue.main.async {
            let imageView = UIImageView(image: image)
            
            self.stackView.addArrangedSubview(imageView)
            
            imageView.translatesAutoresizingMaskIntoConstraints = false
            imageView.widthAnchor.constraint(equalTo: imageView.heightAnchor, multiplier: imageView.image!.size.width / imageView.image!.size.height).isActive = true
        }
    }
    
    func setTurn(turn: Turn) {
        if turnLabel.isHidden && turnImage.isHidden {
            DispatchQueue.main.async {
                self.turnLabel.alpha = 0
                self.turnImage.alpha = 0
                self.turnLabel.isHidden = false
                self.turnImage.isHidden = false
                UIView.animate(withDuration: self.time_animation, animations: {
                    self.turnLabel.alpha = 1
                    self.turnImage.alpha = 1
                }, completion: nil)
            }
        }
        
        switch turn {
        case .user:
            AudioServicesPlaySystemSound(1109)
            turnLabel.text = "It is user's turn"
            turnImage.image = UIImage(named: "ic_user_turn")
        case .robot:
            turnLabel.text = "It is robot's turn"
            turnImage.image = UIImage(named: "ic_robot_turn")
        }
        
        UIView.animate(withDuration: self.time_animation, animations: {
            self.turnImage.transform = CGAffineTransform(scaleX: 1.5, y: 1.5)
        }) { _ in
            UIView.animate(withDuration: self.time_animation) {
                self.turnImage.transform = CGAffineTransform(scaleX: 1, y: 1)
            }
        }
    }
    
    func showAlert(title: String, message: String, done: String, cancel: String?, response: @escaping (DisplayGameAlertResponse) -> ()) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
        let doneAction = UIAlertAction(title: done,
                                   style: .default, handler: { _ in
                                    response(.done)
        })
        alert.addAction(doneAction)
        if let cancel = cancel {
            let cancelAction = UIAlertAction(title: cancel,
                                       style: .default, handler: { _ in
                                        response(.cancel)
            })
            alert.addAction(cancelAction)
        }
        
        self.present(alert, animated: true, completion: nil)
    }

    func addLog(_ text: String) {
        DispatchQueue.main.async {
            self.terminal.text += self.terminal.text == "" ? text : "\n\(text)"
            let bottom = NSMakeRange(self.terminal.text.count - 1, 1)
            self.terminal.scrollRangeToVisible(bottom)
        }
    }
}

extension DisplayGameViewController: DisplayGamePresenterDelegate {
    func detectedFace(_ detected: Bool) {
        imageView.layer.borderColor = detected ? UIColor.detail.cgColor : UIColor.clear.cgColor
    }
    
    func updateImageView(_ image: UIImage) {
        DispatchQueue.main.async {
            self.imageView.image = image
        }
    }
}
