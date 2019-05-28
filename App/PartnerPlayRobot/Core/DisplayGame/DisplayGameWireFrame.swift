//
//  DisplayGameWireFrame.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 26/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import UIKit

class DisplayGameWireFrame {
    static func createDisplayGame() -> UIViewController {
        let viewController = DisplayGameViewController()
        return viewController
    }
    
    static func openDisplayGame(from target: UIViewController) {
        let viewController = createDisplayGame()
        target.present(viewController, animated: true, completion: nil)
    }

    func dismiss(_ viewController: UIViewController) {
        viewController.dismiss(animated: true, completion: nil)
    }
}
