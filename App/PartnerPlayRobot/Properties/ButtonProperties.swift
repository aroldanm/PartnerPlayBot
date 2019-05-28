//
//  ButtonProperties.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 25/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import UIKit

protocol ButtonProperties {
    var background: UIColor? { get }
    var tintColor: UIColor? { get }
    var titleColor: UIColor? { get }
    var title: String? { get }
}
