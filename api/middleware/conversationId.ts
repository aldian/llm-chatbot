import { Request, Response, NextFunction } from 'express';
import dotenv from 'dotenv';
import { NO_CONVERSATION_ID_PROVIDED } from '../config/messages';

dotenv.config();

const conversationIdMiddleware = (req: Request, res: Response, next: NextFunction) => {
    const conversationId = req.headers['conversation_id'] as string;

    if (!conversationId) {
        return res.status(400).json({message: NO_CONVERSATION_ID_PROVIDED});
    }

    next();
};

export default conversationIdMiddleware;