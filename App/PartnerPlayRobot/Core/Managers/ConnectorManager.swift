//
//  ConnectorManager.swift
//  CameraDemo
//
//  Created by Alan Roldán Maillo on 27/04/2019.
//  Copyright © 2019 Alan Roldán Maillo. All rights reserved.
//

import Foundation

enum ConnectionStatus {
    case connected
    case failure
    case disconnected
}

protocol ConnectorManagerDelegate: AnyObject {
    func statusConnectionHasBeenUpdated(_ status: ConnectionStatus)
    func received(message: String)
    func sended(message: String)
}

class ConnectorManager: NSObject, StreamDelegate {
    static let shared = ConnectorManager()
    
    weak var delegate: ConnectorManagerDelegate?
    var timer_timeout: Timer!
    
//    let addr = "192.168.0.26"
    let addr = "172.20.10.2"
    let port = 9876
    
    private let time_out_interval = 10.0
    
    private(set) var status: ConnectionStatus = .disconnected
    
    //Network variables
    private var inStream : InputStream?
    private var outStream: OutputStream?
    
    //Data received
    private var buffer = [UInt8](repeating: 0, count: 1024)
    
    private override init(){}
    
    func stream(_ aStream: Stream, handle eventCode: Stream.Event) {
        switch eventCode {
        case .openCompleted:
            timer_timeout.invalidate()
            addLog("Connected to server")
            updateStatus(.connected)
        case .endEncountered:
            addLog("Connection stopped by server")
            resetAll()
            updateStatus(.disconnected)
        case .errorOccurred:
            timer_timeout.invalidate()
            addLog("ErrorOccurred")
            resetAll()
            updateStatus(.failure)
        case .hasBytesAvailable:
            if aStream == inStream,
                let inStream = inStream {
                receive(input: inStream)
            }
        case .hasSpaceAvailable:
            addLog("")
        default:
            addLog("Code Unknown")
        }
    }

    func begin() {
        let response = SessionResponseModel(code: .begin)
        if let json = response.parseToJson() {
            sendMessage(json)
        }
    }
}

private extension ConnectorManager {
    func receive(input: InputStream) {
        buffer = [UInt8](repeating: 0, count: 1024)
        input.read(&buffer, maxLength: buffer.count)
        if let message = String(bytes: buffer, encoding: .utf8) {
            addLog("Server: \(message)")
            delegate?.received(message: message)
        }
    }

    func addLog(_ text: String) {
        print(text)
    }
    
    func updateStatus(_ status: ConnectionStatus) {
        self.status = status
        delegate?.statusConnectionHasBeenUpdated(status)
    }
    
    func resetAll() {
        inStream?.close()
        inStream?.remove(from: .current, forMode: RunLoop.Mode.default)
        outStream?.close()
        outStream?.remove(from: .current, forMode: RunLoop.Mode.default)
        inStream = nil
        outStream = nil
    }
}

extension ConnectorManager: ConnectorManagerProtocol {
    func connect() {
        addLog("Trying to find \(addr):\(port)...")
        Stream.getStreamsToHost(withName: addr, port: port,
                                inputStream: &inStream,
                                outputStream: &outStream)
        inStream?.delegate = self
        outStream?.delegate = self
        
        inStream?.schedule(in: RunLoop.current, forMode: RunLoop.Mode.default)
        outStream?.schedule(in: RunLoop.current, forMode: RunLoop.Mode.default)
        
        inStream?.open()
        outStream?.open()
        
        buffer = [UInt8](repeating: 0, count: 1024)
        
        timer_timeout = Timer.scheduledTimer(withTimeInterval: time_out_interval, repeats: false) { _ in
            if self.status == .disconnected {
                self.resetAll()
                self.updateStatus(.failure)
            }
        }
    }
    
    func disconnect() {
        let response = SessionResponseModel(code: .exit)
        if let json = response.parseToJson() {
            sendMessage(json)
        }
    }
    
    func sendMessage(_ message: String) {
        sendMessage(message, showLog: false)
    }
    
    func sendMessage(_ message: String, showLog: Bool) {
        guard let outStream = outStream,
            let data : Data = message.data(using: .utf8) else {
                addLog("Can not send it")
                return
        }

        if showLog {
            addLog("You: \(message)")
            delegate?.sended(message: message)
        }

        _ = data.withUnsafeBytes {
            outStream.write($0, maxLength: data.count)
        }
    }
}
