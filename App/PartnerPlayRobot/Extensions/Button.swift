//
//  Button.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 25/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import UIKit
import AudioToolbox

extension UIButton {
    open override var isHighlighted: Bool {
        didSet {
            var alpha: CGFloat = 1.0
            if isHighlighted {
                alpha = 0.7
            }
            self.alpha = alpha
            
            if oldValue != isHighlighted {
                AudioServicesPlaySystemSound(1519)
            }
        }
    }
}
