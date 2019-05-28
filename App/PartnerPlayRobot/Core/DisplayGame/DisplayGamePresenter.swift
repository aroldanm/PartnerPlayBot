//
//  DisplayGamePresenter.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 27/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import UIKit

protocol DisplayGamePresenterDelegate: NSObject {
    func updateImageView(_ image: UIImage)
    func detectedFace(_ detected: Bool)
}

class DisplayGamePresenter {
    typealias View = UIViewController & DisplayGameViewControllerProtocol & DisplayGamePresenterDelegate
    
    weak var viewController: View?
    
    let businessLogic = DisplayGameBusinessLogic()
    let wireFrame = DisplayGameWireFrame()
    let cameraManager = CameraManager()
    
    var currentTurn: Turn?
    var lastActions = [ActionModel]()
    var backgroundColor: UIColor {
        return businessLogic.backgroundColor
    }
    var buttonCloseProperties: ButtonProperties {
        return businessLogic.buttonCloseProperties
    }
    
    func setup() {
        setupView()
        setupCamera()

        businessLogic.delegate = self
        businessLogic.setup()
        businessLogic.begin()
    }

    func dismiss() {
        if let viewController = viewController {
            viewController.showAlert(title: NSLocalizedString("are_sure_title", comment: "The connection will be lost"),
                                     message: NSLocalizedString("are_sure_message", comment: "Are you sure you want to leave?"),
                                     done: NSLocalizedString("yes", comment: "Yes"),
                                     cancel: NSLocalizedString("no", comment: "No")) { response in
                                        if case DisplayGameAlertResponse.done = response {
                                            DispatchQueue.main.async {
                                                self.disconnectAllAndDismiss()
                                            }
                                        }
            }
        }
    }

    func disconnectAllAndDismiss() {
        self.cameraManager.stopSession()
        self.businessLogic.disconnect()
        if let viewController = viewController {
            self.wireFrame.dismiss(viewController)
        }
    }
}

private extension DisplayGamePresenter {
    func setupView() {
        let addr = ConnectorManager.shared.addr
        let port = ConnectorManager.shared.port
        viewController?.addLog("Connected with \(addr):\(port)")
    }
    
    func setupCamera() {
        DispatchQueue.main.async {
            self.cameraManager.delegate = self
            self.cameraManager.startSession()
        }
    }
    
    func isEqual(actions: [ActionModel]) -> Bool {
        if actions.count == lastActions.count {
            var isSame = true
            var i = 0
            while isSame, i < actions.count {
                if let item1 = actions[i] as? ReactionActionModel,
                    let item2 = lastActions[i] as? ReactionActionModel,
                    item1.value == item2.value {
                    isSame = true
                } else {
                    isSame = false
                }
                i += 1
            }
            return isSame
        }
        return false
    }
}

extension DisplayGamePresenter: DisplayGameBusinessLogicDelegate {
    func disconnect() {
        disconnectAllAndDismiss()
    }
    
    func received(message: String) {
        viewController?.addLog(message)
    }
    
    func sended(message: String) {
        viewController?.addLog(message)
    }
    
    func setTurn(turn: Turn) {
        if currentTurn == nil || currentTurn != turn {
            self.currentTurn = turn
            viewController?.setTurn(turn: turn)
        }
    }
    
    func setActions(actions: [ActionModel]) {
        if !isEqual(actions: actions) {
            lastActions = actions
            viewController?.clearActions()
            actions.forEach { item in
                if case ActionCode.reaction = item.code,
                    let reaction = item as? ReactionActionModel {
                    switch reaction.type {
                    case .text:
                        viewController?.addLabelAction(message: reaction.value)
                    case .gif:
                        GifManager.loadRandomGif(reaction.value) { response in
                            if case let GifResponse.success(image) = response {
                                self.viewController?.addGifAction(image: image)
                            }
                        }
                    case .sound:
                        print("sound")
                    }
                }
            }
        }
    }
}

extension DisplayGamePresenter: CameraManagerDelegate {
    func detectedFace(_ detected: Bool) {
        viewController?.detectedFace(detected)
        businessLogic.detectedFace(detected)
    }
    
    func updateCameraImage(_ image: UIImage) {
        viewController?.updateImageView(image)
    }
}
