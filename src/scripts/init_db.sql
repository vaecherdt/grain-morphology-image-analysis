CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    file_name TEXT NOT NULL,
    timestamp TEXT,
    exif TEXT,
    defect TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS grains (
    id SERIAL PRIMARY KEY,
    image_id INTEGER REFERENCES images(id),
    region TEXT,
    cooperative TEXT,
    harvest_information TEXT,
    timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS climate (
    if SERIAL PRIMARY KEY,
    grains_id INTEGER REFERENCES grains(id),
    temperature FLOAT,
    humidity FLOAT,
    weather_conditions TEXT,
    timestamp TIMESTAMP
)