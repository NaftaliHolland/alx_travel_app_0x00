from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random
from django.core.management.base import BaseCommand
#from django_seed import Seed
from listings.models import Booking, Listing, Review
from users.models import User

#seeder = Seed.seeder()

class Command(BaseCommand):
    help = "Adds some initial data to the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Clear existing data (optional - comment out if you want to keep existing data)
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.all().delete()

        # Create Users
        owners = []
        guests = []

        # Create 5 owners
        for i in range(1, 6):
            owner = User.objects.create_user(
                email=f"owner{i}@example.com",
                password="password123",
                first_name=f"Owner{i}",
                last_name=f"LastName{i}",
                role="owner",
            )
            owners.append(owner)
            self.stdout.write(f"Created owner: {owner.email}")

        # Create 10 guests
        for i in range(1, 11):
            guest = User.objects.create_user(
                email=f"guest{i}@example.com",
                password="password123",
                first_name=f"Guest{i}",
                last_name=f"LastName{i}",
                role="guest",
            )
            guests.append(guest)
            self.stdout.write(f"Created guest: {guest.email}")

        # Create Listings
        listings = []
        listing_names = [
            "Cozy Beach House",
            "Mountain Cabin Retreat",
            "Downtown Loft",
            "Lakeside Villa",
            "Urban Studio",
            "Country Farmhouse",
            "Luxury Penthouse",
            "Rustic Cottage",
            "Modern Apartment",
            "Seaside Bungalow",
            "Forest Lodge",
            "City Center Condo",
            "Riverside Retreat",
            "Historic Townhouse",
            "Garden Estate",
        ]

        descriptions = [
            "Perfect getaway with stunning views and modern amenities.",
            "Peaceful retreat surrounded by nature.",
            "Conveniently located near all major attractions.",
            "Spacious and comfortable with all the essentials.",
            "Beautifully decorated and well-maintained property.",
        ]

        for i, name in enumerate(listing_names):
            listing = Listing.objects.create(
                name=name,
                description=random.choice(descriptions),
                price=Decimal(random.randint(50, 500)),
                status=random.choice(["available", "available", "available", "booked"]),
                owner=random.choice(owners),
            )
            listings.append(listing)
            self.stdout.write(f"Created listing: {listing.name}")

        # Create Bookings
        bookings = []
        base_date = timezone.now().date()

        for i in range(20):
            guest = random.choice(guests)
            listing = random.choice(listings)

            # Generate random booking dates
            days_ahead = random.randint(-30, 60)
            start_date = base_date + timedelta(days=days_ahead)
            duration = random.randint(2, 14)
            end_date = start_date + timedelta(days=duration)

            # Determine payment status based on dates
            if start_date < base_date:
                payment_status = random.choice(["paid", "cancelled"])
            else:
                payment_status = random.choice(["pending", "paid"])

            try:
                booking = Booking.objects.create(
                    customer=guest,
                    listing=listing,
                    start_date=start_date,
                    end_date=end_date,
                    payment_status=payment_status,
                )
                bookings.append(booking)
                self.stdout.write(f"Created booking: {guest.email} -> {listing.name}")
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Skipped booking due to error: {e}")
                )

        # Create Reviews (only for past bookings with 'paid' status)
        past_paid_bookings = [
            b for b in bookings if b.end_date < base_date and b.payment_status == "paid"
        ]

        comments = [
            "Great place, highly recommend!",
            "Had an amazing time, will definitely come back.",
            "Clean and comfortable, just as described.",
            "Good value for money.",
            "Nice location but could use some updates.",
            "Perfect for our needs!",
            "Exceeded our expectations.",
            "Would stay here again.",
            "Beautiful property and great host.",
            "Just okay, nothing special.",
        ]

        for booking in past_paid_bookings[:12]:  # Create reviews for some past bookings
            try:
                review = Review.objects.create(
                    customer=booking.customer,
                    booking=booking,
                    rating=random.randint(3, 5),
                    comment=random.choice(comments),
                )
                self.stdout.write(
                    f"Created review: {review.customer.email} rated {review.rating} stars"
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Skipped review due to error: {e}")
                )

        self.stdout.write(
            self.style.SUCCESS("Database seeding completed successfully!")
        )
        self.stdout.write(f"Created {User.objects.count()} users")
        self.stdout.write(f"Created {Listing.objects.count()} listings")
        self.stdout.write(f"Created {Booking.objects.count()} bookings")
        self.stdout.write(f"Created {Review.objects.count()} reviews")
