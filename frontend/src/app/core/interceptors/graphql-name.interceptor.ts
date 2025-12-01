import { HttpInterceptorFn } from '@angular/common/http';

export const graphqlNameInterceptor: HttpInterceptorFn = (req, next) => {
  if (req.url.includes('/graphql') && req.method === 'POST') {
    const body = req.body as any;
    
    if (body && body.operationName) {
      const opName = body.operationName;

      // ASTUCE VISUELLE : On ajoute le nom comme si c'était un dossier
      // Ex: http://127.0.0.1:8000/graphql/GetSidebarModules
      const newReq = req.clone({
        url: `${req.url}/${opName}`
      });

      return next(newReq);
    }
  }
  return next(req);
};