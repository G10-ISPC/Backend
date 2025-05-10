import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AuthService } from './auth.service';
import { environment } from '../../environments/environment';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthService]
    });

    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should authenticate user with valid credentials', () => {
    const mockResponse = {
      token: 'fake-jwt-token',
      user: {
        id: 1,
        username: 'testuser',
        email: 'test@example.com',
        is_staff: false
      }
    };

    service.login('testuser', 'password').subscribe(response => {
      expect(response).toEqual(mockResponse);
      expect(service.isAuthenticated()).toBeTrue();
      expect(service.isAdmin()).toBeFalse();
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/api/login/`);
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);
  });

  it('should register new user successfully', () => {
    const mockResponse = {
      message: 'User registered successfully'
    };

    const userData = {
      username: 'newuser',
      email: 'new@example.com',
      password: 'password123'
    };

    service.register(userData).subscribe(response => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/api/registro/`);
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);
  });

  it('should handle authentication errors', () => {
    const errorResponse = {
      status: 400,
      error: { message: 'Invalid credentials' }
    };

    service.login('wronguser', 'wrongpass').subscribe({
      error: (error) => {
        expect(error.status).toBe(400);
        expect(error.error.message).toBe('Invalid credentials');
      }
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/api/login/`);
    expect(req.request.method).toBe('POST');
    req.flush(errorResponse, { status: 400, statusText: 'Bad Request' });
  });

  it('should handle admin user authentication', () => {
    const mockResponse = {
      token: 'fake-jwt-token',
      user: {
        id: 1,
        username: 'admin',
        email: 'admin@example.com',
        is_staff: true
      }
    };

    service.login('admin', 'password').subscribe(response => {
      expect(response).toEqual(mockResponse);
      expect(service.isAuthenticated()).toBeTrue();
      expect(service.isAdmin()).toBeTrue();
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/api/login/`);
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);
  });

  it('should clear authentication on logout', () => {
    service.logout();
    expect(service.isAuthenticated()).toBeFalse();
    expect(service.isAdmin()).toBeFalse();
  });
}); 