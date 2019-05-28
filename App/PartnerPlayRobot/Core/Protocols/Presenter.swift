//
//  Presenter.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 25/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation
import UIKit

protocol Presenter {
    associatedtype View
    var viewController: View? { get set }
}
