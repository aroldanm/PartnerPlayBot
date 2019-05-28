//
//  ResponseModel.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 12/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

protocol ResponseModel {
    var code: ModelCode { get }
    
    func parseToJson() -> String?
    func dictToJson(_ dictionary: [String: Any]) -> String?
}

extension ResponseModel {
    func dictToJson(_ dictionary: [String: Any]) -> String? {
        guard let jsonData = try? JSONSerialization.data(withJSONObject: dictionary),
            let jsonString = String(data: jsonData, encoding: String.Encoding.ascii) else {
            return nil
        }
        return jsonString
    }
}
