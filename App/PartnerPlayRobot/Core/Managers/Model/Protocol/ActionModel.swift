//
//  ActionModel.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 19/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

enum ActionCode: Int {
    case reaction = 0
    case cheat = 1
    case abort = 2
}

protocol ActionModel {
    var code: ActionCode { get }
    
    static func create(from dictionary: [String: Any]) -> ActionModel?
}

