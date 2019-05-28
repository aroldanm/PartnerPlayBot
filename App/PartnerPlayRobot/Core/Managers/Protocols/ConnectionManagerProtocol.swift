//
//  ConnectorManagerProtocol.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 11/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

protocol ConnectorManagerProtocol {
    func connect()
    func disconnect()
    func sendMessage(_ message: String)
}
