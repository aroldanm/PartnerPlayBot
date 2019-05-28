//
//  DisplayGameBusinessLogic.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 26/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import UIKit

protocol DisplayGameBusinessLogicDelegate: AnyObject {
    func disconnect()
    func received(message: String)
    func sended(message: String)
    func setTurn(turn: Turn)
    func setActions(actions: [ActionModel])
}

class DisplayGameBusinessLogic {
    weak var delegate: DisplayGameBusinessLogicDelegate?
    
    let backgroundColor = UIColor.background
    let buttonCloseProperties = buttonClosePropertiesImpl()
    
    private let faceDetectionStorage = FaceDetectionStorage()
    private let processResponse = ProcessResponse()
    
    struct buttonClosePropertiesImpl: ButtonProperties {
        var tintColor: UIColor? = .content
        var background: UIColor?
        var titleColor: UIColor?
        var title: String?
    }
    
    func setup() {
        processResponse.delegate = self
        ConnectorManager.shared.delegate = self
    }
    
    func detectedFace(_ detected: Bool) {
        faceDetectionStorage.push(detected: detected)
    }
    
    func getDetectionStatistics() -> Float {
        return faceDetectionStorage.pop()
    }

    func disconnect() {
        ConnectorManager.shared.disconnect()
    }
    
    func begin() {
        ConnectorManager.shared.begin()
    }
}

private extension DisplayGameBusinessLogic {
    func procesateResponse(message: String) {
        if let query = QueryModelImpl.parseFromJson(message) {
            processResponse.execute(query, faceDetection: getDetectionStatistics())
        }
    }
}

extension DisplayGameBusinessLogic: ConnectorManagerDelegate {
    func statusConnectionHasBeenUpdated(_ status: ConnectionStatus) {
        delegate?.disconnect()
    }
    
    func received(message: String) {
        if message != "" {
            delegate?.received(message: message)
            procesateResponse(message: message)
        }
    }
    
    func sended(message: String) {
        delegate?.sended(message: message)
    }
}

extension DisplayGameBusinessLogic: ProcessResponseDelegate {
    func didBeResponse(response: ResponseModel) {
        if let jsonString = response.parseToJson() {
            ConnectorManager.shared.sendMessage(jsonString, showLog: true)
        }
    }

    func setTurn(turn: Turn) {
        delegate?.setTurn(turn: turn)
    }
    
    func setActions(actions: [ActionModel]) {
        delegate?.setActions(actions: actions)
    }
}
