//
//  FaceDetectionStorage.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 11/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

class FaceDetectionStorage {
    private var allDetections: Float = 0.0
    private var trueDetections: Float = 0.0
    private var count_access = 0
    
    private let RESET_AT = 15
    
    func push(detected: Bool) {
        if detected {
            trueDetections += 1
        }
        allDetections += 1
    }

    func pop() -> Float {
        count_access += 1
        var evaluation: Float = 0
        if trueDetections > 0 {
            evaluation = trueDetections / allDetections
        }
        reset()
        return evaluation
    }
}

private extension FaceDetectionStorage {
    func reset() {
        if count_access >= RESET_AT {
            count_access = 0
            allDetections = 0.0
            trueDetections = 0.0
        }
    }
}
