const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

// Get command line arguments
const args = process.argv.slice(2);
const caption = args[0];
const imagePath = args[1];
const groupName = args[2] || "Nandi Content";

if (!caption || !imagePath) {
    console.error('Usage: node whatsapp_sender.js "caption" "image_path" [group_name]');
    process.exit(1);
}

// Validate image path
if (!fs.existsSync(imagePath)) {
    console.error(`Image file not found: ${imagePath}`);
    process.exit(1);
}

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    }
});

client.on('qr', (qr) => {
    console.log('QR RECEIVED', qr);
    qrcode.generate(qr, { small: true });
});

client.on('ready', async () => {
    console.log('Client is ready!');
    
    try {
        // Find the group by name
        const chats = await client.getChats();
        const group = chats.find(chat => chat.name === groupName && chat.isGroup);
        
        if (!group) {
            console.error(`Group "${groupName}" not found`);
            console.log('Available groups:', chats.filter(chat => chat.isGroup).map(chat => chat.name));
            process.exit(1);
        }
        
        // Send caption
        await group.sendMessage(caption);
        console.log('Caption sent successfully');
        
        // Send image
        const media = MessageMedia.fromFilePath(imagePath);
        await group.sendMessage(media);
        console.log('Image sent successfully');
        
        process.exit(0);
    } catch (error) {
        console.error('Error sending message:', error);
        process.exit(1);
    }
});

client.on('auth_failure', (msg) => {
    console.error('Authentication failed:', msg);
    process.exit(1);
});

client.on('disconnected', (reason) => {
    console.log('Client was disconnected:', reason);
    process.exit(1);
});

client.initialize(); 