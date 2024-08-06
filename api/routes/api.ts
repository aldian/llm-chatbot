import express, { Router } from "express";
import conversationIdMiddleware from "../middleware/conversationId";
import { fetchConversations, getConversation, initConversation, sendPrompt } from '../controller/chatBotController';

const router = Router();
router.use(express.json());

router.get("/conversations", fetchConversations);
router.get("/conversation",  conversationIdMiddleware, getConversation);
router.post("/init-conversation", initConversation);
router.post("/conversation", conversationIdMiddleware, sendPrompt);

export default router;