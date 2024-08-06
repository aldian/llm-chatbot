import express, { Express } from 'express';
import apiRoutes from './routes/api';
import errorHandler from './middleware/errorHandler';

export const createServer = (): Express => {
  const app: Express = express();
  app.use('', apiRoutes);
  app.use(errorHandler);
  return app;
};

const app = createServer();
const port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log(`[server]: Server is running at http://localhost:${port}`);
});

export default app;