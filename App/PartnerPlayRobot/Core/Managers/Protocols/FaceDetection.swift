//
//  FaceDetection.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 11/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import UIKit
import Vision

protocol FaceDetection {
    func launchDetection(image: UIImage)
    func handleDetection(request: VNRequest, errror: Error?)
}
