#!/usr/bin/env python




def main():
   
    print(f'inserito utente {peer.session_id}')

    peer.delete()
    print(f'rimosso utente {peer.session_id}')

if __name__ == '__main__':
    main()
