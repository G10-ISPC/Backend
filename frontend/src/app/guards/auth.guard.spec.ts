import { TestBed } from '@angular/core/testing';
import { Router, ActivatedRouteSnapshot } from '@angular/router';
import { AuthGuard } from './auth.guard';
import { AuthService } from '../services/auth.service';

describe('AuthGuard', () => {
  let guard: AuthGuard;
  let authService: jasmine.SpyObj<AuthService>;
  let router: jasmine.SpyObj<Router>;

  beforeEach(() => {
    const authServiceSpy = jasmine.createSpyObj('AuthService', ['isAuthenticated', 'isAdmin']);
    const routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    TestBed.configureTestingModule({
      providers: [
        AuthGuard,
        { provide: AuthService, useValue: authServiceSpy },
        { provide: Router, useValue: routerSpy }
      ]
    });

    guard = TestBed.inject(AuthGuard);
    authService = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    router = TestBed.inject(Router) as jasmine.SpyObj<Router>;
  });

  it('should be created', () => {
    expect(guard).toBeTruthy();
  });

  it('should allow access to protected routes when user is authenticated', () => {
    authService.isAuthenticated.and.returnValue(true);
    const route = new ActivatedRouteSnapshot();
    route.data = {};

    expect(guard.canActivate(route)).toBeTrue();
    expect(router.navigate).not.toHaveBeenCalled();
  });

  it('should redirect to login when user is not authenticated', () => {
    authService.isAuthenticated.and.returnValue(false);
    const route = new ActivatedRouteSnapshot();

    expect(guard.canActivate(route)).toBeFalse();
    expect(router.navigate).toHaveBeenCalledWith(['/login']);
  });

  it('should allow access to admin routes when user is admin', () => {
    authService.isAuthenticated.and.returnValue(true);
    authService.isAdmin.and.returnValue(true);
    const route = new ActivatedRouteSnapshot();
    route.data = { requiresAdmin: true };

    expect(guard.canActivate(route)).toBeTrue();
    expect(router.navigate).not.toHaveBeenCalled();
  });

  it('should redirect to unauthorized when non-admin tries to access admin route', () => {
    authService.isAuthenticated.and.returnValue(true);
    authService.isAdmin.and.returnValue(false);
    const route = new ActivatedRouteSnapshot();
    route.data = { requiresAdmin: true };

    expect(guard.canActivate(route)).toBeFalse();
    expect(router.navigate).toHaveBeenCalledWith(['/unauthorized']);
  });
}); 