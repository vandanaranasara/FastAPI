from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from ..database import SessionLocal, get_db
from ..models import Todo, User
from ..schemas import TodoCreate, TodoOut
from ..auth import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/todos", tags=["Todos"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid user")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/", response_model=TodoOut)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_todo = Todo(title=todo.title, user_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.get("/", response_model=list[TodoOut])
async def get_todos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Todo).filter(Todo.user_id == current_user.id).all()


@router.put("/{todo_id}", response_model=TodoOut)
async def update_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.completed = not todo.completed
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}
