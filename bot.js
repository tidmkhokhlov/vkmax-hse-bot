import { Bot } from '@maxhub/max-bot-api';
import dotenv from 'dotenv';

dotenv.config();

const bot = new Bot(process.env.MAXBOT_TOKEN);

const HELLO = "👋 Добро пожаловать!\n" +
    "\n" +
    "Я — виртуальный помощник для абитуриентов Высшей школы экономики в Нижнем Новгороде. Рад вам помочь! 😊\n" +
    "\n" +
    "Чем я могу быть полезен:\n" +
    "\n" +
    "🎓 Ответить на ваши вопросы о поступлении, экзаменах, баллах и сроках.\n" +
    "\n" +
    "📱 Показать список программ и их краткое описание в нашем мини-приложении.\n" +
    "\n" +
    "Просто задайте свой вопрос, и я постараюсь найти на него ответ!"

async function handleUserMessage(userMessage) {
    try {
        const response = await fetch('http://localhost:8000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: userMessage
            })
        });

        const data = await response.json();
        return data.answer;

    } catch (error) {
        console.error('API Error:', error);
        return 'Извините, сервис временно недоступен.';
    }
}

// Обработчик для команды '/start'
bot.command('start', (ctx) => ctx.reply(HELLO));

// Обработчик для любого другого сообщения
bot.on('message_created', async (ctx, next) => {
    const answer = await handleUserMessage(ctx.message.body.text)
    return ctx.reply(answer);
});

// Запуск
bot.start();
