import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { HTTP_INTERCEPTORS, HttpClient } from '@angular/common/http';
import { AuthInterceptor } from './auth.interceptor';
import { AuthService } from '../services/auth.service';

describe('AuthInterceptor', () => {
  let httpClient: HttpClient;
  let httpMock: HttpTestingController;
  let authService: jasmine.SpyObj<AuthService>;

  beforeEach(() => {
    const authServiceSpy = jasmine.createSpyObj('AuthService', ['getToken']);

    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
      ]
    });

    httpClient = TestBed.inject(HttpClient);
    httpMock = TestBed.inject(HttpTestingController);
    authService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(httpClient).toBeTruthy();
  });

  it('should add authorization header to protected API requests', () => {
    const token = 'fake-jwt-token';
    authService.getToken.and.returnValue(token);

    httpClient.get('/api/protected-route').subscribe();

    const httpRequest = httpMock.expectOne('/api/protected-route');
    expect(httpRequest.request.headers.has('Authorization')).toBeTrue();
    expect(httpRequest.request.headers.get('Authorization')).toBe(`Bearer ${token}`);
  });

  it('should not add authorization header to public routes', () => {
    authService.getToken.and.returnValue(null);

    httpClient.get('/api/public-route').subscribe();

    const httpRequest = httpMock.expectOne('/api/public-route');
    expect(httpRequest.request.headers.has('Authorization')).toBeFalse();
  });

  it('should handle multiple protected requests with different tokens', () => {
    const token1 = 'first-token';
    const token2 = 'second-token';

    authService.getToken.and.returnValues(token1, token2);

    httpClient.get('/api/protected-route1').subscribe();
    httpClient.get('/api/protected-route2').subscribe();

    const httpRequest1 = httpMock.expectOne('/api/protected-route1');
    const httpRequest2 = httpMock.expectOne('/api/protected-route2');

    expect(httpRequest1.request.headers.get('Authorization')).toBe(`Bearer ${token1}`);
    expect(httpRequest2.request.headers.get('Authorization')).toBe(`Bearer ${token2}`);
  });

  it('should handle unauthorized responses', () => {
    authService.getToken.and.returnValue('fake-token');

    httpClient.get('/api/protected-route').subscribe({
      error: (error) => {
        expect(error.status).toBe(401);
      }
    });

    const httpRequest = httpMock.expectOne('/api/protected-route');
    httpRequest.flush('Unauthorized', { status: 401, statusText: 'Unauthorized' });
  });
}); 