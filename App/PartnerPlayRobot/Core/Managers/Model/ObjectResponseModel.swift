//
//  ObjectResponseModel.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 14/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

class ObjectResponseModel: ResponseModel {
    var code: Int = -1
    var faceDetection: Float = 1.0
    
    init(_ dictionary: [String : Any]) {
        guard let code = dictionary["code"] as? Int else {
            return
        }
        self.code = code
    }
    
    func parseToJson() -> String? {
        let dictionary: [String: Any] = ["code" : code,
                                         "faceDetection" : faceDetection]
        if let jsonData = try? JSONSerialization.data(withJSONObject: dictionary),
            let jsonString = String(data: jsonData, encoding: String.Encoding.ascii) {
            return jsonString
        }
        return nil
    }
}
