//
//  GifManager.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 19/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation
import UIKit

enum GifResponse {
    case success(UIImage)
    case url(String)
    case failure(Error)
    
    enum Error: Swift.Error {
        case notDataAvaliable
        case notInternet
        case error
    }
}

class GifManager {
    
    static func loadRandomGif(_ text: String, completion: @escaping (GifResponse) -> ()) {
        getRandomGif(text) { response in
            switch response {
            case .success(let image):
                completion(.success(image))
            case .failure(let error):
                completion(.failure(error))
            case .url(let url):
                let request = URLRequest(url: URL(string: url)!)
                let task = URLSession.shared.dataTask(with: request) { data, response, error in
                    if error != nil {
                        completion(.failure(.error))
                        return
                    }
                    if let data = data,
                        let image = UIImage.gif(data: data) {
                        completion(.success(image))
                    }
                }
                task.resume()
            }
        }
    }
}

private extension GifManager {
    static func getRandomGif(_ text: String, completion: @escaping (GifResponse) -> ()) {
        let pathurl = "https://api.giphy.com/v1/gifs/random?api_key=R0cCSgQE6YQiOYacHIAja51S80uqMflr&tag=\(text)"
        
        guard let url = URL(string: pathurl) else {
            return
        }
        
        var request = URLRequest(url: url)
        request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "GET"
        request.timeoutInterval = 30.0
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            
            if let error = error as? URLError,
                case URLError.Code.notConnectedToInternet = error.code {
                completion(.failure(.notInternet))
                return
            }
            
            // check for fundamental networking error
            guard let data = data, error == nil else {
                completion(.failure(.notDataAvaliable))
                return
            }
            
            // check for http errors
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                completion(.failure(.error))
                return
            }
            
            guard let result = try? JSONSerialization.jsonObject(with: data, options:.allowFragments),
                let json = result as? [String: Any],
                json.count > 0 else {
                    completion(.failure(.notDataAvaliable))
                    return
            }
            if let item = json["data"] as? [String: Any],
                let images = item["images"] as? [String: Any],
                let original = images["original"] as? [String: Any],
                let imageUrl = original["url"] as? String {
                completion(.url(imageUrl))
            }
        }
        task.resume()
    }
}
