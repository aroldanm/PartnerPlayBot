//
//  CameraProtocol.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 11/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation
import AVFoundation

protocol CameraProtocol {
    var session: AVCaptureSession? { get }
    
    func startSession()
    func stopSession()
}
