//
//  QueryModel.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 19/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

enum ModelCode: Int {
    case error = -1
    case normal = 0
    case cheat = 1
    case cheat_finished = 2
    case begin = 200
    case exit = 255
}

enum Turn: Int {
    case user = 0
    case robot = 1
}

protocol QueryModel {
    var code: ModelCode { get }
    var turn: Turn { get }
    var actions: [ActionModel] { get }
    
    static func parseFromJson(_ message: String) -> QueryModel?
    static func jsonToDict(_ message: String) -> [String: Any]?
}

extension QueryModel {
    static func jsonToDict(_ message: String) -> [String: Any]? {
        let text = message.replacingOccurrences(of: "\0", with: "")
        guard let data = text.data(using: .utf8),
            let json = try? JSONSerialization.jsonObject(with: data, options: []),
            let dictionary = json as? [String : Any] else {
                return nil
        }
        return dictionary
    }
}
