from src.schemas.users_schemas import UserRequestAdd, UserAdd, User, UserHashedPassword
from src.schemas.pagination import PaginationParams
from src.schemas.bookings_schemas import Booking, BookingAdd, BookingsPrintOut
from src.schemas.amenities_schemas import Amenity, AmenitiesPrintOut, PaginatedAmenitiesPrintOut, RoomAmenityAdd, RoomAmenity
from src.schemas.rooms_schemas import HotelBasic, Room, RoomWithRelations, RoomCreate, RoomCreateInternal, RoomUpdate, RoomUpdateInternal, RoomPatch
from src.schemas.facilities_schemas import Facility, FacilitiesPrintOut, PaginatedFacilitiesPrintOut, RoomFacilityAdd, RoomFacility
from src.schemas.hotels_schemas import Hotel, HotelUpdate, HotelPatch, HotelsPrintOut, PaginatedHotelsPrintOut