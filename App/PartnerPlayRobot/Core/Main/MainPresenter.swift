//
//  MainPresenter.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 25/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation
import UIKit

class MainPresenter: Presenter {
    typealias View = UIViewController & MainViewControllerProtocol
    weak var viewController: View?
    let businessLogic = MainBusinessLogic()
    let wireFrame = MainWireFrame()
    
    var connectionStatus: ConnectionStatus {
        return businessLogic.connectionStatus
    }

    var backgroundColor: UIColor {
        return businessLogic.backgroundColor
    }
    var beginButtonProperties: ButtonProperties {
        return businessLogic.beginButtonProperties
    }
    var connectButtonProperties: ButtonProperties {
        return businessLogic.connectButtonProperties
    }
    var disconnectButtonProperties: ButtonProperties {
        return businessLogic.disconnectButtonProperties
    }
    var titleProperties: LabelProperties {
        return businessLogic.titleProperties
    }
    var welcomeProperties: LabelProperties {
        return businessLogic.welcomeProperties
    }
    
    func setupView() {
        viewController?.begin = {
            if let viewController = self.viewController {
                switch self.connectionStatus {
                case .connected:
                    self.wireFrame.presentDisplayGame(from: viewController)
                case .disconnected,
                     .failure:
                    self.businessLogic.connect()
                }
            }
        }
        
        viewController?.disconnect = {
            self.businessLogic.disconnect()
            self.viewController?.changeStatus(to: self.connectionStatus)
        }
    }
    
    func setupDelegates() {
        businessLogic.delegate = self
        businessLogic.setup()
    }

    func loadResources() {
        businessLogic.connect()
    }
}

extension MainPresenter: MainBusinessLogicDelegate {
    func connectionUpdate(status: ConnectionStatus) {
        self.viewController?.loadCompleted()
        if case ConnectionStatus.failure = status {
            self.viewController?.showErrorConnection()
        }
        self.viewController?.changeStatus(to: self.connectionStatus)
    }
}

