//
//  ResponseModelImpl.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 19/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

class ResponseModelImpl: ResponseModel {
    private(set) var code: ModelCode
    let faceDetection: Float
    
    init(code: ModelCode, faceDetection: Float ) {
        self.code = code
        self.faceDetection = faceDetection
    }
    
    func parseToJson() -> String? {
        let dictionary: [String: Any] = ["code" : code.rawValue,
                                         "faceDetection" : faceDetection]
        return dictToJson(dictionary)
    }
}
