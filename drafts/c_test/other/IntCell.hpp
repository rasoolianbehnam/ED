class IntCell
{
    public:
        explicit IntCell( int initialValue = 0 )
        { storedValue = new int( initialValue ); }

        IntCell( const IntCell & rhs )
        { storedValue = new int( *rhs.storedValue ); }

        ~IntCell( ) { delete storedValue; }

        const IntCell & operator=( const IntCell & rhs ) {
            if( this != &rhs )
                *storedValue = *rhs.storedValue;
            return *this;
        }

        const IntCell & operator*( const IntCell & rhs ) {
            int a = *storedValue * *rhs.storedValue;
            IntCell *b;
            b = new IntCell(a);
            return *b;
        }

        const IntCell & operator+( const IntCell & rhs ) {
            int a = *storedValue + *rhs.storedValue;
            IntCell *b;
            b = new IntCell(a);
            return *b;
        }

        int getValue( ) const
        { return *storedValue; }
        void setValue( int val )
        { *storedValue = val; }
    private:
        int *storedValue;
};
