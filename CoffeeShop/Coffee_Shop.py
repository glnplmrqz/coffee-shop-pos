"""
1. Caramel Macchiato – ₱130
2. Caffè Mocha – ₱120
3. Caffè Latte – ₱110
4. Cappuccino – ₱110
5. Chocolate Cappuccino – ₱125
6. Brewed Coffee – ₱80
7. Espresso (single shot) – ₱70
8. Espresso Macchiato – ₱90
9. White Mocha – ₱130
10. Signature Hot Chocolate – ₱115
"""
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class CoffeeShop:
    def __init__(self, window):
        self.window = window
        self.window.title("Coffee Shop POS System")
        self.window.state('zoomed')
        self.window.configure(bg='#f5f5dc')

        # Coffee Menu, Prices, and Images File Path
        self.coffeeMenu = [
            ("Caramel Macchiato", 130, "Caramel Macchiato.jpg"),
            ("Caffe Mocha", 120, "Caffè Mocha.jpg"),
            ("Caffe Latte", 110, "Caffè Latte.jpg"),
            ("Cappucino", 110, "Cappuccino.jpg"),
            ("Chocolate Cappucino", 125, "Chocolate Cappuccino.jpg"),
            ("Brewed Coffee", 80, "Brewed Coffee.jpg"),
            ("Espresso", 70, "Espresso.jpg"),
            ("Espresso Macchiato", 90, "Espresso Macchiato.jpg"),
            ("White Mocha", 130, "White Mocha.jpg"),
            ("Signature Hot Chocolate", 115, "Signature Hot Chocolate.jpg")
        ]

        # For Displaying Order Items
        self.orderItems = []
        # Iterating Images and the Name of the Images
        self.coffeeImages = {}

        # Calling Function
        self.loadImages()
        self.setupUserInterFace()

    def loadImages(self):
        # Make the Images path robust relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        imageDirectory = os.path.join(base_dir, "Images")

        for coffeeMenu, prices, imageFile in self.coffeeMenu:  # Iterating
            imagePath = os.path.join(imageDirectory, imageFile)
            try:
                if os.path.exists(imagePath):
                    images = Image.open(imagePath)
                    images = images.resize((100, 100), Image.LANCZOS)
                    photos = ImageTk.PhotoImage(images)
                    self.coffeeImages[coffeeMenu] = photos
                else:
                    # Create a placeholder if the file isn't found
                    self.createPlaceholderImage(coffeeMenu)
            except Exception as e:
                # If Pillow fails to open/convert, still make a placeholder
                print(f"Error loading '{imagePath}': {e}")
                self.createPlaceholderImage(coffeeMenu)

    def createPlaceholderImage(self, coffeeMenu):
        images = Image.new('RGB', (100, 100), color='#d9b99b')
        draw = ImageDraw.Draw(images)

        # Try a common system font; fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()

        # Draw the coffee name (abbreviated if too long) centered
        abbreviatedName = coffeeMenu[:12] + "..." if len(coffeeMenu) > 12 else coffeeMenu
        draw.text((50, 50), abbreviatedName, fill="black", font=font, anchor="mm")

        photos = ImageTk.PhotoImage(images)
        self.coffeeImages[coffeeMenu] = photos

    def setupUserInterFace(self):
        # Title Label
        titleLabel = Label(self.window,
                           text="☕ Kapihan Koh Toh Boy!",
                           font=('Poppins', 24, 'bold'),
                           bg='#f5f5dc', fg='#6f4e37')
        titleLabel.pack(pady=25)

        # Main Frame
        mainFrame = Frame(self.window, bg='#f5f5dc')
        mainFrame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Configure grid weights (Current Order bigger than Coffee Menu)
        mainFrame.columnconfigure(0, weight=1)   # Coffee Menu smaller
        mainFrame.columnconfigure(1, weight=2)   # Current Order larger
        mainFrame.rowconfigure(0, weight=1)

        # Menu Frame -> Display Coffee Menu
        menuFrame = LabelFrame(mainFrame,
                               text="☕Coffee Menu",
                               font=('Poppins', 14, 'bold'),
                               bg='#f5f5dc', fg='#6f4e37',
                               padx=5, pady=10,
                               labelanchor='n')
        menuFrame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Order Frame -> Display Order
        orderFrame = LabelFrame(mainFrame,
                                text="🛒Current Order",
                                font=('Poppins', 14, 'bold'),
                                bg='#f5f5dc', fg='#6f4e37',
                                padx=10, pady=10,
                                labelanchor='n')
        orderFrame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # Build content
        self.createMenuButtons(menuFrame)
        self.createOrderDisplay(orderFrame)

        # Footer Frame for total + buttons
        footerFrame = Frame(self.window, bg='#f5f5dc')
        footerFrame.pack(fill=X, padx=20, pady=10)

        # Total Label — keep as attribute so updateTotal works
        self.totalLabel = Label(footerFrame,
                                text="Total: ₱0.00",
                                font=('Poppins', 16, 'bold'),
                                bg='#f5f5dc', fg='#6f4e37')
        self.totalLabel.pack(side=LEFT)

        # Button Frame
        buttonFrame = Frame(footerFrame, bg='#f5f5dc')
        buttonFrame.pack(side=RIGHT)

        # Create Buttons
        checkoutButton = Button(buttonFrame,
                                text="Checkout",
                                font=("Poppins", 12),
                                bg='#6f4e37', fg='White', 
                                activebackground='#6f4e37', activeforeground='White',
                                padx=20, pady=5,
                                command=self.showPaymentWindow)
        checkoutButton.pack(side=LEFT, padx=5)

        clearOrder = Button(buttonFrame,
                            text="Clear Order",
                            font=("Poppins", 12),
                            bg='red', fg='white', 
                            activebackground='red', activeforeground='white',
                            padx=20, pady=5,
                            command=self.clearOrder)
        clearOrder.pack(side=RIGHT, padx=5)

    def createMenuButtons(self, parent):
        # Canvas + Scrollbar for scrolling menu
        canvas = Canvas(parent, bg='#f5f5dc', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollableFrame = Frame(canvas, bg='#f5f5dc')

        # Keep scrollregion in sync
        scrollableFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollableFrame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        # PACK them (this was missing before)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Build each menu row
        for i, (coffeeMenu, prices, imageFile) in enumerate(self.coffeeMenu):
            btnFrame = Frame(scrollableFrame,
                             bg='#f5f5dc',
                             highlightbackground='#d9b99b',
                             highlightthickness=1, bd=0)
            btnFrame.pack(fill=X, padx=5, pady=5)

            # Coffee Icon
            if coffeeMenu in self.coffeeImages:
                iconLabel = Label(btnFrame, image=self.coffeeImages[coffeeMenu], bg='#f5f5dc')

                iconLabel.image = self.coffeeImages[coffeeMenu]
                iconLabel.pack(side=LEFT, padx=10)
            else:
                iconLabel = Label(btnFrame, text="☕", font=("Poppins", 16),
                                  bg='#f5f5dc', fg='#6f4e37')
                iconLabel.pack(side=LEFT, padx=10)

            # Coffee name and price
            infoFrame = Frame(btnFrame, bg='#f5f5dc')
            infoFrame.pack(side=LEFT, fill=X, expand=True)

            nameLabel = Label(infoFrame, text=coffeeMenu, font=("Poppins", 12),
                              bg='#f5f5dc', fg='#6f4e37', anchor="w")
            nameLabel.pack(fill=X)

            priceLabel = Label(infoFrame, text=f"₱{prices}", font=("Poppins", 10),
                               bg='#f5f5dc', fg='#8b4513')
            priceLabel.pack(fill=X)

            # Add button
            addButton = Button(btnFrame, text="Add", font=("Poppins", 10),
                               bg='#6f4e37', fg='white', 
                               activebackground='#6f4e37', activeforeground='white',
                               padx=10,
                               command=lambda n=coffeeMenu, p=prices: self.addToOrder(n, p))
            addButton.pack(side=RIGHT, padx=10)

    def createOrderDisplay(self, parent):
        canvas = Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollableFrame = Frame(canvas, bg='white')

        scrollableFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollableFrame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Header Row
        headerFrame = Frame(scrollableFrame, bg='#6f4e37')
        headerFrame.pack(fill=X, pady=(0, 5))

        itemHeader = Label(headerFrame, text="Item", font=("Poppins", 12, "bold"),
                           bg='#6f4e37', fg='white', width=30, anchor="w")
        itemHeader.pack(side=LEFT, padx=10)

        qtyHeader = Label(headerFrame, text="Quantity", font=("Poppins", 12, "bold"),
                          bg='#6f4e37', fg='white', width=10)
        qtyHeader.pack(side=LEFT)

        priceHeader = Label(headerFrame, text="Price", font=("Poppins", 12, "bold"),
                            bg='#6f4e37', fg='white', width=15)
        priceHeader.pack(side=LEFT)

        actionHeader = Label(headerFrame, text="Action", font=("Poppins", 12, "bold"),
                             bg='#6f4e37', fg='white', width=10)
        actionHeader.pack(side=LEFT)

        self.orderFrame = scrollableFrame
        self.orderCanvas = canvas

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # Add Order Functions
    def addToOrder(self, coffeeMenu, prices):
        # Check if item already exists in order
        for i, (itemName, itemPrice, quantity) in enumerate(self.orderItems):
            if itemName == coffeeMenu:
                self.orderItems[i] = (coffeeMenu, prices, quantity + 1)
                self.updateOrderDisplay()
                return

        # Add new item to order
        self.orderItems.append((coffeeMenu, prices, 1))
        self.updateOrderDisplay()

    def updateOrderDisplay(self):
        # Clear the order display (except header)
        for widget in self.orderFrame.winfo_children()[1:]:
            widget.destroy()

        # Add each order item to the display
        for i, (itemName, itemPrice, quantity) in enumerate(self.orderItems):
            itemFrame = Frame(self.orderFrame, bg='white' if i % 2 == 0 else '#f8f8f8')
            itemFrame.pack(fill=X, pady=1)

            # Item image (smaller version)
            if itemName in self.coffeeImages:
                iconLabel = Label(itemFrame, image=self.coffeeImages[itemName], bg=itemFrame['bg'])
                iconLabel.image = self.coffeeImages[itemName]  # Keep a reference
                iconLabel.pack(side=LEFT, padx=5)
            else:
                iconLabel = Label(itemFrame, text="☕", font=("Poppins", 12),
                                  bg=itemFrame['bg'], fg='#6f4e37')
                iconLabel.pack(side=LEFT, padx=5)

            # Item name
            nameLabel = Label(itemFrame, text=itemName, font=("Poppins", 11),
                              bg=itemFrame['bg'], fg='#6f4e37', width=25, anchor="w")
            nameLabel.pack(side=LEFT, padx=5)

            # Quantity with buttons to adjust
            qtyFrame = Frame(itemFrame, bg=itemFrame['bg'])
            qtyFrame.pack(side=LEFT)

            minusButton = Button(qtyFrame, text="-", font=("Poppins", 8),
                                 bg='#d9b99b', fg='black', width=2,
                                 command=lambda idx=i: self.decreaseQuantity(idx))
            minusButton.pack(side=LEFT)

            qtyLabel = Label(qtyFrame, text=str(quantity), font=("Poppins", 11),
                             bg=itemFrame['bg'], fg='black', width=5)
            qtyLabel.pack(side=LEFT)

            plusButton = Button(qtyFrame, text="+", font=("Poppins", 8),
                                bg='#d9b99b', fg='black', width=2,
                                command=lambda idx=i: self.increaseQuantity(idx))
            plusButton.pack(side=LEFT)

            # Price
            totalPrice = itemPrice * quantity
            priceLabel = Label(itemFrame, text=f"₱{totalPrice}", font=("Poppins", 11),
                               bg=itemFrame['bg'], fg='#8b4513', width=15)
            priceLabel.pack(side=LEFT)

            # Remove button
            removeButton = Button(itemFrame, text="Remove", font=("Poppins", 9),
                                  bg='#333', fg='white',
                                  activebackground='#333', activeforeground='white', padx=5,
                                  command=lambda idx=i: self.removeItem(idx))
            removeButton.pack(side=LEFT, padx=10)

        # Update total
        self.updateTotal()

        # Update scroll region
        self.orderCanvas.configure(scrollregion=self.orderCanvas.bbox("all"))

    def increaseQuantity(self, index):
        itemName, itemPrice, quantity = self.orderItems[index]
        self.orderItems[index] = (itemName, itemPrice, quantity + 1)
        self.updateOrderDisplay()

    def decreaseQuantity(self, index):
        itemName, itemPrice, quantity = self.orderItems[index]
        if quantity > 1:
            self.orderItems[index] = (itemName, itemPrice, quantity - 1)
        else:
            self.removeItem(index)
        self.updateOrderDisplay()

    def removeItem(self, index):
        self.orderItems.pop(index)
        self.updateOrderDisplay()

    def updateTotal(self):
        total = sum(price * quantity for _, price, quantity in self.orderItems)
        self.totalLabel.config(text=f"Total: ₱{total:.2f}")

    def clearOrder(self):
        if self.orderItems:
            if messagebox.askyesno("Confirm", "Are you sure you want to clear the order?"):
                self.orderItems = []
                self.updateOrderDisplay()

    def checkout(self):
        if not self.orderItems:
            messagebox.showwarning("Warning", "Your order is empty!")
            return
        else:
            # Clear the order
            self.orderItems = []
            self.showPaymentWindow()
            self.updateOrderDisplay()

    def showPaymentWindow(self):
        if not self.orderItems:
            messagebox.showwarning("Warning", "Your order is empty!")
            return
        
        # Create payment window
        paymentWindow = Toplevel(self.window)
        paymentWindow.title("Payment")
        paymentWindow.geometry("400x300")
        paymentWindow.configure(bg='#f5f5dc')
        paymentWindow.grab_set()  # Make window modal
        
        # Calculate total
        total = sum(price * quantity for _, price, quantity in self.orderItems)
        
        # Payment title
        titleLabel = Label(paymentWindow, text="Payment Details", 
                           font=('Poppins', 18, "bold"), bg='#f5f5dc', fg='#6f4e37')
        titleLabel.pack(pady=15)
        
        # Order total
        totalLabel = Label(paymentWindow, text=f"Total Amount: ₱{total:.2f}", 
                           font=("Poppins", 14), bg='#f5f5dc', fg='#6f4e37')
        totalLabel.pack(pady=5)
        
        # Cash amount field (shown only when cash is selected)
        cashFrame = Frame(paymentWindow, bg='#f5f5dc')
        cashFrame.pack(pady=10)
        
        cashLabel = Label(cashFrame, text="Cash Amount:", 
                          font=("Poppins", 12), bg='#f5f5dc', fg='#6f4e37')
        cashLabel.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        
        cashVar = StringVar()
        cashEntry = Entry(cashFrame, textvariable=cashVar, font=("Poppins", 12), width=15)
        cashEntry.grid(row=0, column=1, padx=5, pady=5)
        
        # Change label
        changeLabel = Label(cashFrame, text="Change: ₱0.00", 
                            font=("Arial", 12), bg='#f5f5dc', fg='#6f4e37')
        changeLabel.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Function to calculate change
        def calculateChange():
            if cashVar.get():
                try:
                    cashAmount = float(cashVar.get())
                    change = cashAmount - total
                    
                    if change >= 0:
                        changeLabel.config(text=f"Change: ₱{change:.2f}", fg='green')
                        proceedButton.config(state=NORMAL)  
                    else:
                        changeLabel.config(text=f"Additional: ₱{-change:.2f}", fg='red')
                        proceedButton.config(state=DISABLED)
                except ValueError:
                    changeLabel.config(text="Invalid amount", fg='red')
                    proceedButton.config(state=DISABLED)
            else:
                proceedButton.config(state=DISABLED)

        # Update change when cash amount changes
        cashVar.trace('w', lambda *args: calculateChange())

        def processPayment():
            cashAmount = float(cashVar.get())

            # Process successful cash payment
            change = cashAmount - total
                
            # Generate receipt
            receipt = "========== ☕ Kapihan Koh Toh Boy! ==========\n"
            receipt += "Thank you for your order!\n\n"
                
            for itemName, itemPrice, quantity in self.orderItems:
                receipt += f"{itemName} x{quantity} - ₱{itemPrice * quantity}\n"
                
            receipt += f"\nTotal: ₱{total:.2f}\n"
            receipt += f"Cash Received: ₱{cashAmount:.2f}\n"
            receipt += f"Change: ₱{change:.2f}\n"
            receipt += "====================================="
                
            # Show receipt
            messagebox.showinfo("Payment Successful", 
                            f"Payment received!\nChange: ₱{change:.2f}\n\n{receipt}")
                
            # Clear the order
            self.orderItems = []
            self.updateOrderDisplay()
                
            # Close payment window
            paymentWindow.destroy()
     # Button frame
        buttonFrame = Frame(paymentWindow, bg='#f5f5dc')
        buttonFrame.pack(pady=15)

        proceedButton = Button(buttonFrame, text="Proceed", 
                               font=("Arial", 12), bg='#6f4e37', fg='white',
                               activebackground='#6f4e37', activeforeground='white', 
                               padx=20, pady=5, command=processPayment)
        proceedButton.pack(side=LEFT, padx=10)
        
        # Cancel button
        cancelButton = Button(buttonFrame, text="Cancel", 
                              font=("Arial", 12), bg='red', fg='white', 
                              activebackground='red', activeforeground='white',
                              padx=20, pady=5, command=paymentWindow.destroy)
        cancelButton.pack(side=LEFT, padx=10)    

# Create the main window
window = Tk()
app = CoffeeShop(window)
window.mainloop()