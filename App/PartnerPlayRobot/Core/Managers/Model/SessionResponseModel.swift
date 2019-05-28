//
//  SesionResponseModel.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 13/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

class SessionResponseModel: ResponseModel {
    var code: ModelCode
    
    init(code: ModelCode) {
        self.code = code
    }
    
    func parseToJson() -> String? {
        let dictionary: [String: Any] = ["code" : code.rawValue]
        if let jsonData = try? JSONSerialization.data(withJSONObject: dictionary),
            let jsonString = String(data: jsonData, encoding: String.Encoding.ascii) {
            return jsonString
        }
        return nil
    }
}
