class Card():
    
    '''
    This is the class for each super hero card
    '''
    
    def __init__(self,vals):
        '''
        Recieves a list and creates a card for each of the elements
        
        If the stat value is None, it records it as a 0
        '''
        
        # card values
        self.name = vals[0]
        if vals[1] == None:
            self.intel = 0
        else:
            self.intel = vals[1]
        if vals[2] == None:
            self.strength = 0
        else:
            self.strength = vals[2]
        if vals[3] == None:
            self.speed = 0
        else:    
            self.speed = vals[3]
        if vals[4] == None:
            self.durability = 0   
        else:
            self.durability = vals[4]
        if vals[5] == None:
            self.power = 0
        else:
            self.power = vals[5]
        if vals[6] == None:
            self.combat = 0    
        else:
            self.combat = vals[6]
        self.image = vals[7]
        self.publisher = vals[8]
        self.alignment = vals[9]
        self.alias = vals[10]

        # values of stats ratings
        self.intel_rating = None
        self.strength_rating = None
        self.speed_rating = None
        self.durabilty_rating = None
        self.power_rating = None
        self.combat_rating = None
        self.stat_order = []
        
        
    def show_card_details(self):
        """
        Displays the card details to terminal (used for debugging)
        """
        print(f"""
              Name: {self.name}, 
              Intelligence: {self.intel} ({self.intel_rating})
              Strength: {self.strength} ({self.strength_rating})
              Speed: {self.speed} ({self.speed_rating})
              Durability: {self.durability} ({self.durabilty_rating})
              Power: {self.power} ({self.power_rating})
              Combat: {self.combat} ({self.combat_rating})
              Stat order: {self.stat_order}
              """)
        
        
    def all_blank(self):
        """
        Idenfitise if the all the card stats are blank
        """
        if self.intel == 0 and \
            self.strength == 0 and \
            self.speed == 0 and \
            self.durability == 0 and \
            self.power == 0 and \
            self.combat == 0:
            return True
        else:
            return False
        
    
    def get_rankings(self,deck):
        """
        Establishes the relative ranking of the card stats in a deck 
        by iterating over the deck and checking the each of the card's
        stats relative rating against other cards.
        """
        
        # set inital ranking
        self.intel_rating = 1
        self.strength_rating = 1
        self.speed_rating = 1
        self.durabilty_rating = 1
        self.power_rating = 1
        self.combat_rating = 1
        
        # check each card in deck, when a stat is greater than the
        # card's stat, it's ranking is dropped in that stat
        for card in deck:
            if self.intel < card.intel:
                self.intel_rating += 1
            if self.strength < card.strength:
                self.strength_rating += 1
            if self.speed < card.speed:
                self.speed_rating += 1
            if self.durability < card.durability:
                self.durabilty_rating += 1
            if self.power < card.power:
                self.power_rating += 1
            if self.combat < card.combat:
                self.combat_rating += 1
        
        # take rankings and sort them         
        self.sort_stats()
                
    
    def sort_stats(self):
        '''
        For a card, creates a dictionary, then sorts that dictionary 
        on the rating.
        
        Finally the stat names are written to stat_order, so the highest
        ranking is first.
        '''
        temp_stats = {
            "intel": self.intel_rating,
            "strength": self.strength_rating,
            "speed": self.speed_rating,
            "durability": self.durabilty_rating,
            "power": self.power_rating,
            "combat": self.combat_rating
        }
        
        # sort stats on ranking
        sorted_stats = sorted(temp_stats.items(),key=lambda x:x[1])
        
        # write stat name to stat_order
        for index in sorted_stats:
            self.stat_order.append(index[0])