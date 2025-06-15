#!/bin/bash

echo "🚀 Starting Ubuntu 24.04 Setup..."

# Update system
echo "📝 Updating package lists..."
sudo apt update -y

echo "⬆️ Upgrading packages..."
sudo apt upgrade -y

# Install PostgreSQL (instead of MySQL for better Ubuntu compatibility)
echo "🗄️ Installing PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
echo "🔧 Setting up database..."
sudo -u postgres psql -c "CREATE DATABASE csye6225db;"
sudo -u postgres psql -c "CREATE USER csyeuser WITH PASSWORD 'securepass123';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE csye6225db TO csyeuser;"

# Create application group
echo "👥 Creating application group..."
sudo groupadd csye6225group

# Create application user
echo "👤 Creating application user..."
sudo useradd -r -g csye6225group -s /bin/bash csyeuser

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /opt/csye6225

# Create application files
echo "📄 Setting up application files..."
sudo mkdir -p /opt/csye6225/app
sudo mkdir -p /opt/csye6225/logs

# Download and setup Node.js
echo "📦 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 for process management
sudo npm install -y pm2 -g

# Set permissions
echo "🔐 Setting permissions..."
sudo chown -R csyeuser:csye6225group /opt/csye6225
sudo chmod -R 755 /opt/csye6225

echo "✅ Setup completed successfully!"
echo "📊 Summary:"
echo "   - PostgreSQL installed and running"
echo "   - Database 'csye6225db' created"
echo "   - User 'csyeuser' created"
echo "   - Application directory: /opt/csye6225"
echo "   - Node.js installed"