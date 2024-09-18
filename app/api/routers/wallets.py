from fastapi.routing import APIRouter


router = APIRouter(
    prefix="/wallets",
    tags=["wallets"],
)


@router.get("/")
async def get_wallet():
    return {"success": True}
