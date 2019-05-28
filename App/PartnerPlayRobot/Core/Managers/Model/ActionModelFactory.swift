//
//  ActionModelFactory.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 19/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

class ActionModelFactory {
    static func make(elements: [String]) -> [ActionModel] {
        var array = [ActionModel]()
        elements.forEach { item in
            if let dictionary = jsonToDict(item),
                let code_int = dictionary["code"] as? Int,
                let code = ActionCode(rawValue: code_int) {
                
                switch code {
                case .reaction:
                    if let action = ReactionActionModel.create(from: dictionary) {
                        array.append(action)
                    }
                case .cheat:
                    print("cheat action")
                case .abort:
                    print("abort action")
                }
            }
        }
        return array
    }
}

private extension ActionModelFactory {
    static func jsonToArray(_ message: String) -> [String]? {
        let text = message.replacingOccurrences(of: "\0", with: "")
        guard let data = text.data(using: .utf8),
            let json = try? JSONSerialization.jsonObject(with: data, options: []),
            let array = json as? [String] else {
                return nil
        }
        return array
    }
    
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
