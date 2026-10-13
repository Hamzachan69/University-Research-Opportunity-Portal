-- Database: research_portal
CREATE DATABASE IF NOT EXISTS research_portal;
USE research_portal;

-- Table: opportunities
CREATE TABLE IF NOT EXISTS opportunities (
    id                    INT           NOT NULL AUTO_INCREMENT,
    title                 VARCHAR(200)  NOT NULL,
    description           TEXT          NOT NULL,
    research_area         VARCHAR(100)  NOT NULL,
    faculty_name          VARCHAR(150)  NOT NULL,
    department            VARCHAR(150)  NOT NULL,
    required_skills       VARCHAR(500)  DEFAULT NULL,
    available_positions   INT           NOT NULL DEFAULT 1,
    application_deadline  DATE          NOT NULL,
    status                ENUM('Open', 'Closed') NOT NULL DEFAULT 'Open',
    created_at            TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Sample data
INSERT INTO opportunities 
    (title, description, research_area, faculty_name, department, required_skills, available_positions, application_deadline, status)
VALUES
    ('AI for Healthcare Diagnostics', 
     'Using deep learning models to detect diseases early from medical imaging data.', 
     'Artificial Intelligence', 'Dr. Ahmed Khan', 'Computer Science', 
     'Python, TensorFlow, Data Analysis', 2, '2026-12-15', 'Open'),

    ('Wireless Sensor Networks for Smart Agriculture', 
     'Designing low-power sensor networks to monitor soil and crop health in real time.', 
     'Networking', 'Dr. Sara Malik', 'Computer Science', 
     'C++, Embedded Systems, IoT', 3, '2026-11-30', 'Open'),

    ('Natural Language Processing for Urdu Text', 
     'Building NLP models for sentiment analysis and text classification in the Urdu language.', 
     'Machine Learning', 'Dr. Bilal Hussain', 'Computer Science', 
     'Python, NLP, PyTorch', 1, '2026-10-20', 'Open'),

    ('Blockchain-Based Voting System', 
     'Researching secure and transparent voting mechanisms using blockchain technology.', 
     'Cybersecurity', 'Dr. Ayesha Raza', 'Software Engineering', 
     'Solidity, Blockchain, Cryptography', 2, '2026-09-25', 'Closed'),

    ('Human-Robot Interaction Study', 
     'Studying how humans interact with assistive robots in elderly care settings.', 
     'Robotics', 'Dr. Usman Tariq', 'Electrical Engineering', 
     'ROS, Python, Robotics', 2, '2026-12-01', 'Open');

