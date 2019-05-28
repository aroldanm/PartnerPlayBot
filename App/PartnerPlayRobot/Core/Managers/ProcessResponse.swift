//
//  ProcessResponse.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 19/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

protocol ProcessResponseDelegate: AnyObject {
    func didBeResponse(response: ResponseModel)
    func setTurn(turn: Turn)
    func setActions(actions: [ActionModel])
}

class ProcessResponse {
    weak var delegate: ProcessResponseDelegate?
    
    func execute(_ query: QueryModel, faceDetection: Float) {
        delegate?.setTurn(turn: query.turn)
        delegate?.setActions(actions: query.actions)
        
        //Always Same response
        let response = ResponseModelImpl(code: query.code, faceDetection: faceDetection)
        delegate?.didBeResponse(response: response)
    }
}
