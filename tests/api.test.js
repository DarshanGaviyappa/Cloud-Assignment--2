const request = require('supertest');
const app = require('../app');

describe('API Integration Tests', () => {
  
  // Health check tests
  describe('GET /health', () => {
    test('should return 200 and health status', async () => {
      const response = await request(app)
        .get('/health')
        .expect(200);
      
      expect(response.body.status).toBe('OK');
      expect(response.body.message).toBe('Application is healthy');
    });
  });

  // Users API tests - Success scenarios
  describe('Users API - Success Cases', () => {
    test('GET /api/users should return 200 and users array', async () => {
      const response = await request(app)
        .get('/api/users')
        .expect(200);
      
      expect(response.body).toHaveProperty('users');
      expect(Array.isArray(response.body.users)).toBe(true);
    });

    test('POST /api/users should create user successfully', async () => {
      const userData = {
        name: 'John Doe',
        email: `test${Date.now()}@example.com`
      };
      
      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);
      
      expect(response.body.name).toBe(userData.name);
      expect(response.body.email).toBe(userData.email);
      expect(response.body.id).toBeDefined();
    });
  });

  // Users API tests - Failure scenarios
  describe('Users API - Failure Cases', () => {
    test('POST /api/users should return 400 when name is missing', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'test@example.com' })
        .expect(400);
      
      expect(response.body.error).toBe('Name is required');
    });

    test('POST /api/users should return 400 when email is missing', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ name: 'John Doe' })
        .expect(400);
      
      expect(response.body.error).toBe('Email is required');
    });

    test('POST /api/users should return 409 for duplicate email', async () => {
      const userData = {
        name: 'Jane Doe',
        email: 'duplicate@example.com'
      };
      
      // Create first user
      await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);
      
      // Try to create duplicate
      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(409);
      
      expect(response.body.error).toBe('Email already exists');
    });
  });

  // 404 tests
  describe('404 Error Handling', () => {
    test('should return 404 for non-existent routes', async () => {
      await request(app)
        .get('/api/nonexistent')
        .expect(404);
    });
  });
});