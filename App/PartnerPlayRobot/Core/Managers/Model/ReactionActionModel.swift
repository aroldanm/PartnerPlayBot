//
//  ReactionActionModel.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 19/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

enum ReactionType:Int {
    case text = 0
    case sound = 1
    case gif = 2
}

class ReactionActionModel: ActionModel {
    private(set) var code: ActionCode
    let type: ReactionType
    let value: String
    
    init(code: ActionCode, type: ReactionType, value: String) {
        self.code = code
        self.type = type
        self.value = value
    }
    
    static func create(from dictionary: [String: Any]) -> ActionModel? {
        guard let code_int = dictionary["code"] as? Int,
            let code = ActionCode(rawValue: code_int),
            let type_int = dictionary["type"] as? Int,
            let type = ReactionType(rawValue: type_int) else {
                return nil
        }
        let value = (dictionary["value"] as? String) ?? ""
        return ReactionActionModel(code: code, type: type, value: value)
    }
}
