//
//  MainBusinessLogic.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 26/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import UIKit

enum LoadMainResponse {
    case success
    case failure
}

protocol MainBusinessLogicDelegate: AnyObject {
    func connectionUpdate(status: ConnectionStatus)
}

class MainBusinessLogic {
    let backgroundColor = UIColor.background
    let beginButtonProperties = ButtonPropertiesImpl()
    let connectButtonProperties = ConnectButtonPropertiesImpl()
    let disconnectButtonProperties = disconnectButtonPropertiesImpl()
    let titleProperties = TitlePropertiesImpl()
    let welcomeProperties = WelcomePropertiesImpl()
    
    weak var delegate: MainBusinessLogicDelegate?
    
    var connectionStatus: ConnectionStatus {
        return ConnectorManager.shared.status
    }
    
    struct ButtonPropertiesImpl: ButtonProperties {
        var tintColor: UIColor?
        var background: UIColor? = .detail
        var titleColor: UIColor? = .content
        var title: String? = NSLocalizedString("begin", comment: "Begin")
    }
    
    struct ConnectButtonPropertiesImpl: ButtonProperties {
        var tintColor: UIColor?
        var background: UIColor? = .disconnected
        var titleColor: UIColor? = .content
        var title: String? = NSLocalizedString("reconnect_button", comment: "Reconnect")
    }
    
    struct disconnectButtonPropertiesImpl: ButtonProperties {
        var tintColor: UIColor? = .content
        var background: UIColor?
        var titleColor: UIColor?
        var title: String?
    }
    
    struct TitlePropertiesImpl: LabelProperties {
        var textColor: UIColor? = UIColor.content
        var text: String? = NSLocalizedString("title_project", comment: "PartnetPlayRobot")
    }
    
    struct WelcomePropertiesImpl: LabelProperties {
        var textColor: UIColor? = TitlePropertiesImpl().textColor
        var text: String? = NSLocalizedString("welcome_to", comment: "Welcome to")
    }

    func setup() {
        ConnectorManager.shared.delegate = self
    }
    
    func connect() {
        ConnectorManager.shared.connect()
    }

    func disconnect() {
        ConnectorManager.shared.disconnect()
    }
}

extension MainBusinessLogic: ConnectorManagerDelegate {
    func received(message: String) {
    }
    
    func sended(message: String) {
    }
    
    func statusConnectionHasBeenUpdated(_ status: ConnectionStatus) {
        delegate?.connectionUpdate(status: status)
    }
}
