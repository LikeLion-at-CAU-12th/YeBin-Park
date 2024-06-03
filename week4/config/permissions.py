from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    "게시물 작성자만 접근가능"
    def has_object_permission(self,request,view,obj):
        if request.user.is_authenticated:
            if request.user==obj.user:
                return True
            return False
        else:
            return False
        
class IsKey(BasePermission):
    def has_permission(self,request,view):
       if request.headers.get('LION')=='LION':
           return True
       return False
        
        
class CombinedPermission(IsOwner, IsKey): #두 조건을 모두 가져야하는 상속 custum permission
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)