//
//  QueryModelImpl.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 19/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

class QueryModelImpl: QueryModel {
    private(set) var code: ModelCode
    private(set) var turn: Turn
    private(set) var actions: [ActionModel]
    
    init(code: ModelCode, turn: Turn, actions: [ActionModel]) {
        self.code = code
        self.turn = turn
        self.actions = actions
    }
    
    static func parseFromJson(_ message: String) -> QueryModel? {
        guard let dictionary = jsonToDict(message),
            let code_int = dictionary["code"] as? Int,
            let code = ModelCode(rawValue: code_int),
            let turn_int = dictionary ["turn"] as? Int,
            let turn = Turn(rawValue: turn_int) else {
                return nil
        }
        var actions = [ActionModel]()
        if let elements = dictionary["actions"] as? [String] {
            actions = ActionModelFactory.make(elements: elements)
        }
        return QueryModelImpl(code: code, turn: turn, actions: actions)
    }
}
