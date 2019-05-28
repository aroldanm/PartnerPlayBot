//
//  CameraManager.swift
//  PartnerPlayRobot
//
//  Created by Alan Roldán Maillo on 11/05/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation
import UIKit
import AVFoundation
import Vision

protocol CameraManagerDelegate: AnyObject {
    func updateCameraImage(_ image: UIImage)
    func detectedFace(_ detected: Bool)
}

class CameraManager: NSObject {
    var session: AVCaptureSession?

    weak var delegate: CameraManagerDelegate?

    lazy var faceDetectionRequest: VNDetectFaceRectanglesRequest = {
        let faceLandmarksRequest = VNDetectFaceRectanglesRequest(completionHandler: { [weak self] request, error in
            self?.handleDetection(request: request, errror: error)
        })
        return faceLandmarksRequest
    }()
    
    override init() {
        super.init()

        session = AVCaptureSession()
        
        //setup input
        let device =  AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .front)
        let input = try! AVCaptureDeviceInput(device: device!)
        session?.addInput(input)
        
        //setup output
        let output = AVCaptureVideoDataOutput()
        output.videoSettings = [kCVPixelBufferPixelFormatTypeKey as AnyHashable as! String: kCVPixelFormatType_32BGRA]
        output.setSampleBufferDelegate(self, queue: DispatchQueue.main)
        session?.addOutput(output)
    }
}

private extension CameraManager {
    func getImageFromSampleBuffer(sampleBuffer: CMSampleBuffer) ->UIImage? {
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else {
            return nil
        }
        CVPixelBufferLockBaseAddress(pixelBuffer, .readOnly)
        let baseAddress = CVPixelBufferGetBaseAddress(pixelBuffer)
        let width = CVPixelBufferGetWidth(pixelBuffer)
        let height = CVPixelBufferGetHeight(pixelBuffer)
        let bytesPerRow = CVPixelBufferGetBytesPerRow(pixelBuffer)
        let colorSpace = CGColorSpaceCreateDeviceRGB()
        let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedFirst.rawValue | CGBitmapInfo.byteOrder32Little.rawValue)
        guard let context = CGContext(data: baseAddress, width: width, height: height, bitsPerComponent: 8, bytesPerRow: bytesPerRow, space: colorSpace, bitmapInfo: bitmapInfo.rawValue) else {
            return nil
        }
        guard let cgImage = context.makeImage() else {
            return nil
        }
        let image = UIImage(cgImage: cgImage, scale: 1, orientation:.right)
        CVPixelBufferUnlockBaseAddress(pixelBuffer, .readOnly)
        return image
    }
}

extension CameraManager: CameraProtocol {
    func startSession() {
        session?.startRunning()
    }
    
    func stopSession() {
        session?.stopRunning()
    }
}

extension CameraManager: FaceDetection {
    func launchDetection(image: UIImage) {
        let orientation = image.coreOrientation()
        guard let coreImage = CIImage(image: image) else { return }
        
        DispatchQueue.global().async {
            let handler = VNImageRequestHandler(ciImage: coreImage, orientation: orientation)
            do {
                try handler.perform([self.faceDetectionRequest])
            } catch {
                print("Failed to perform detection .\n\(error.localizedDescription)")
            }
        }
    }
    
    func handleDetection(request: VNRequest, errror: Error?) {
        DispatchQueue.main.async { [weak self] in
            if let observations = request.results as? [VNFaceObservation] {
                self?.delegate?.detectedFace(observations.count > 0)
            }
        }
    }
}

extension CameraManager: AVCaptureVideoDataOutputSampleBufferDelegate {
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        guard let outputImage = getImageFromSampleBuffer(sampleBuffer: sampleBuffer) else {
            return
        }
        delegate?.updateCameraImage(outputImage)
        launchDetection(image: outputImage)
    }
}

extension UIImage {
    func coreOrientation() -> CGImagePropertyOrientation {
        switch imageOrientation {
        case .up : return .up
        case .upMirrored: return .upMirrored
        case .down: return .down // 0th row at bottom, 0th column on right  - 180 deg rotation
        case .downMirrored : return .downMirrored// 0th row at bottom, 0th column on left   - vertical flip
        case .leftMirrored : return .leftMirrored // 0th row on left,   0th column at top
        case .right : return .right // 0th row on right,  0th column at top    - 90 deg CW
        case .rightMirrored : return .rightMirrored // 0th row on right,  0th column on bottom
        case .left : return .left // 0th row on left,   0th column at bottom - 90 deg CCW
        default: return .up
        }
    }
}
