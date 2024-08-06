import { Request, Response, NextFunction } from "express";
import ApiError from '../entities/ApiError';
import {
  MISSING_REQUIRED_FIELDS,
  FAILED_TO_FETCH_DATA,
} from '../config/messages';

/*
export const updateUserData = async (req: Request, res: Response, next: NextFunction) => {
  let { id, ...userData } = req.body;
  
  if (!userData.name) {
    return next(new ApiError(400, MISSING_REQUIRED_FIELDS));
  }
  
  const isUpdate = !!id;
  if (!id) {
    id = uuidv4();
  }
  
  try {
    const docRef = db.collection(collectionName).doc(id);

    await docRef.set(userData);
  
    if (isUpdate) {
      res.status(200).json({ message: USER_UPDATED, id });
    } else {
      res.status(201).json({ message: USER_CREATED, id });
    }
  } catch (error) {
    console.log("Error: ", error);
    next(new ApiError(500, FAILED_TO_UPDATE_DATA));
  }
};
*/

export const fetchConversations = async (req: Request, res: Response, next: NextFunction) => {
  try {
    let response = await fetch(`${process.env.LLM_CHATBOT_BASE_URL}/conversations`);

    const data = await response.json();
    return res.json(data);
  } catch (error) {
    console.log("Error: ", error);
    next(new ApiError(500, FAILED_TO_FETCH_DATA));
  }
};

export const getConversation = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const headers = new Headers({
    'conversation_id': req.headers['conversation_id'] as string
    });
    const options = {
        method: 'GET',
        headers,
    };
    let response = await fetch(`${process.env.LLM_CHATBOT_BASE_URL}/conversation`, options);

    const data = await response.json();
    return res.json(data);
  } catch (error) {
    console.log("Error: ", error);
    next(new ApiError(500, FAILED_TO_FETCH_DATA));
  }
};

export const initConversation = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const options = {
        method: 'POST',
    };
    let response = await fetch(`${process.env.LLM_CHATBOT_BASE_URL}/init-conversation`, options);

    const conversationId = await response.text();
    return res.send(conversationId);
  } catch (error) {
    console.log("Error: ", error);
    next(new ApiError(500, FAILED_TO_FETCH_DATA));
  }
};

export const sendPrompt = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const headers = new Headers({
        "Content-Type": "application/json",
        'conversation_id': req.headers['conversation_id'] as string
    });
    const options = {
        method: 'POST',
        headers,
        body: JSON.stringify(req.body), 
    };
    let response = await fetch(`${process.env.LLM_CHATBOT_BASE_URL}/conversation`, options);
    const answer = await response.text();
    return res.send(answer);
  } catch (error) {
    console.log("Error: ", error);
    next(new ApiError(500, FAILED_TO_FETCH_DATA));
  }
};