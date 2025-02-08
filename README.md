# RX-SAT Monitoring System

## Overview
A web-based monitoring system designed for satellite receivers (RX-SAT) in broadcasting networks. This application provides real-time monitoring of satellite receiver parameters across multiple locations using SNMP protocol.

## Features
- **Real-time Monitoring**: Live updates of receiver status and parameters
- **SNMP Integration**: Automated data collection from satellite receivers
- **Server-Sent Events (SSE)**: Real-time updates without page refresh
- **Responsive Web Interface**: Clean, modern dashboard design
- **Multi-location Support**: Monitors receivers across different sites
- **Automatic Status Indicators**: Visual status representation
- **Parameter Tracking**: Monitors multiple technical parameters simultaneously

## Key Parameters Monitored
- Signal Strength (Campo Ricevuto)
- Signal-to-Noise Ratio (SNR)
- Link Margin
- Frequency
- ISI (Input Stream Identifier)
- Firmware Version
- Overall Device Status

## Technical Specifications

### Backend
- **Framework**: Flask (Python)
- **SNMP Library**: pysnmp
- **Data Stream**: Server-Sent Events (SSE)
- **Network Protocol**: SNMP v1

### Frontend
- **Framework**: Bootstrap 5
- **JavaScript**: jQuery
- **Real-time Updates**: EventSource API
- **Styling**: Custom CSS with responsive design

## System Requirements
- Python 3.x
- Flask
- pysnmp
- Modern web browser with SSE support

- ![rxscan](https://github.com/user-attachments/assets/532db097-5ad1-4f0e-b0a9-ea11b8a0109e)
