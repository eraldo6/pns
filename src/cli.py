"""
Command Line Interface (CLI) for Privacy Network System
Provides interactive commands for all system functionalities
"""

import sys
from typing import List, Optional
from datetime import datetime


class PrivacyNetworkCLI:
    """Interactive command-line interface for the Privacy Network System"""
    
    def __init__(self, system):
        self.system = system
        self.running = True
    
    def run(self):
        """Run the interactive CLI"""
        print("Euromask - Interactive CLI")
        print("=" * 50)
        print("Type 'help' for available commands")
        print("Type 'exit' to quit")
        print()
        
        while self.running:
            try:
                user_input = input("\nPNS> ").strip()
                if not user_input:
                    continue
                
                self.process_command(user_input)
                
            except EOFError:
                print("\nGoodbye!")
                break
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def process_command(self, command: str):
        """Process user command"""
        parts = command.split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == 'help':
            self.show_help()
        elif cmd == 'exit' or cmd == 'quit':
            self.running = False
            print("Goodbye!")
        elif cmd == 'status':
            self.show_status()
        elif cmd == 'wallet':
            self.handle_wallet_commands(args)
        elif cmd == 'token':
            self.handle_token_commands(args)
        elif cmd == 'voucher':
            self.handle_voucher_commands(args)
        elif cmd == 'transfer':
            self.handle_transfer_commands(args)
        elif cmd == 'offline':
            self.handle_offline_commands(args)
        elif cmd == 'compliance':
            self.handle_compliance_commands(args)
        elif cmd == 'ledger':
            self.handle_ledger_commands(args)
        elif cmd == 'zkp':
            self.handle_zkp_commands(args)
        elif cmd == 'export':
            self.handle_export_commands(args)
        elif cmd == 'demo':
            self.run_demo()
        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' for available commands")
    
    def show_help(self):
        """Show help information"""
        help_text = """
Euromask - Available Commands
==============================================

System Commands:
  status                    - Show system status
  help                      - Show this help
  exit/quit                 - Exit the CLI
  demo                      - Run comprehensive demo

Wallet Commands:
  wallet create             - Create a new wallet
  wallet list               - List all wallets
  wallet info <id>          - Show wallet details
  wallet balance <id>       - Show wallet balance

Token Commands:
  token issue <wallet_id> <value>  - Issue token to wallet
  token list                        - List all tokens
  token info <id>                   - Show token details
  token balance <wallet_id>         - Show wallet's tokens

Voucher Commands:
  voucher issue <wallet_id> <limit> - Issue voucher to wallet
  voucher list                       - List all vouchers
  voucher info <id>                  - Show voucher details
  voucher available <wallet_id>      - Show available vouchers

Transfer Commands:
  transfer <sender> <receiver> <token_id> [voucher_id]  - Execute transfer
  transfer list                       - List all transactions
  transfer info <id>                  - Show transaction details
  transfer anonymous <sender> <receiver> <token_id> <voucher_id>  - Anonymous transfer

Offline Commands:
  offline create <sender> <receiver> <token_id> [voucher_id]  - Create offline transaction
  offline sign <offline_id> <wallet_id> <signature>           - Sign offline transaction
  offline sync <offline_id>                                   - Sync with ledger
  offline list                                                 - List offline transactions

Compliance Commands:
  compliance list             - List AML entries
  compliance stats            - Show compliance statistics
  compliance export           - Export AML report

Ledger Commands:
  ledger list                 - List ledger entries
  ledger stats                - Show ledger statistics
  ledger query <params>       - Query ledger
  ledger export               - Export ledger data

ZKP Commands:
  zkp range <wallet_id> <min> <max>     - Generate range proof
  zkp verify <proof_id>                 - Verify proof
  zkp list                               - List all proofs
  zkp stats                              - Show ZKP statistics

Export Commands:
  export all                - Export all system data
  export aml                - Export AML report
  export ledger             - Export ledger data
  export zkp                - Export ZKP proofs

Examples:
  wallet create
  token issue wallet1 50
  voucher issue wallet1 100
  transfer wallet1 wallet2 token1 voucher1
  offline create wallet1 wallet2 token1
  zkp range wallet1 0 100
  export all
        """
        print(help_text)
    
    def show_status(self):
        """Show system status"""
        print("\nSystem Status:")
        print("=" * 30)
        
        # Wallet status
        wallets = self.system.wallet_manager.list_wallets()
        print(f"Wallets: {len(wallets)}")
        
        # Token status
        tokens = self.system.token_manager.list_all_tokens()
        total_value = sum(token.value for token in tokens)
        print(f"Tokens: {len(tokens)} (€{total_value})")
        
        # Voucher status
        vouchers = self.system.voucher_manager.list_all_vouchers()
        available_vouchers = self.system.voucher_manager.get_unused_vouchers()
        print(f"Vouchers: {len(vouchers)} ({len(available_vouchers)} available)")
        
        # Transaction status
        transactions = self.system.transaction_engine.list_all_transactions()
        anonymous_transactions = self.system.transaction_engine.get_anonymous_transactions()
        print(f"Transactions: {len(transactions)} ({len(anonymous_transactions)} anonymous)")
        
        # AML status
        aml_entries = self.system.compliance_manager.get_aml_entries()
        print(f"AML Flagged: {len(aml_entries)}")
        
        # Offline status
        offline_txs = self.system.offline_manager.list_all_offline_transactions()
        pending_offline = self.system.offline_manager.get_pending_offline_transactions()
        print(f"Offline: {len(offline_txs)} ({len(pending_offline)} pending)")
        
        # ZKP status
        zkp_proofs = self.system.zkp_manager.list_all_proofs()
        print(f"ZKP Proofs: {len(zkp_proofs)}")
    
    def handle_wallet_commands(self, args: List[str]):
        """Handle wallet-related commands"""
        if not args:
            print("Usage: wallet <command> [args]")
            return
        
        cmd = args[0].lower()
        
        if cmd == 'create':
            wallet = self.system.wallet_manager.create_wallet()
            print(f"Created wallet: {wallet.wallet_id}")
            print(f"   Public Key: {wallet.public_key[:16]}...")
        
        elif cmd == 'list':
            wallets = self.system.wallet_manager.list_wallets()
            if not wallets:
                print("📭 No wallets found")
                return
            
            print(f"\nWallets ({len(wallets)}):")
            for wallet in wallets:
                tokens = self.system.token_manager.get_tokens_by_owner(wallet.wallet_id)
                total_value = sum(token.value for token in tokens)
                print(f"  {wallet.wallet_id[:8]}... - €{total_value} ({len(tokens)} tokens, {wallet.voucher_balance} vouchers)")
        
        elif cmd == 'info':
            if len(args) < 2:
                print("Usage: wallet info <wallet_id>")
                return
            
            wallet_id = args[1]
            wallet = self.system.wallet_manager.get_wallet(wallet_id)
            if not wallet:
                print(f"Wallet {wallet_id} not found")
                return
            
            tokens = self.system.token_manager.get_tokens_by_owner(wallet_id)
            total_value = sum(token.value for token in tokens)
            
            print(f"\nWallet Details:")
            print(f"  ID: {wallet.wallet_id}")
            print(f"  Public Key: {wallet.public_key}")
            print(f"  Token Balance: €{total_value} ({len(tokens)} tokens)")
            print(f"  Voucher Balance: {wallet.voucher_balance}")
            
            if tokens:
                print(f"  Tokens:")
                for token in tokens:
                    print(f"    {token.token_id[:8]}... - €{token.value}")
        
        elif cmd == 'balance':
            if len(args) < 2:
                print("Usage: wallet balance <wallet_id>")
                return
            
            wallet_id = args[1]
            tokens = self.system.token_manager.get_tokens_by_owner(wallet_id)
            total_value = sum(token.value for token in tokens)
            
            print(f"\nWallet Balance: €{total_value}")
            print(f"   Tokens: {len(tokens)}")
            for token in tokens:
                print(f"     {token.token_id[:8]}... - €{token.value}")
        
        else:
            print(f"Unknown wallet command: {cmd}")
    
    def handle_token_commands(self, args: List[str]):
        """Handle token-related commands"""
        if not args:
            print("Usage: token <command> [args]")
            return
        
        cmd = args[0].lower()
        
        if cmd == 'issue':
            if len(args) < 3:
                print("Usage: token issue <wallet_id> <value>")
                return
            
            wallet_id = args[1]
            try:
                value = int(args[2])
            except ValueError:
                print("Value must be a number")
                return
            
            try:
                token = self.system.token_manager.issue_token(value, wallet_id)
                print(f"Issued token: {token.token_id[:8]}... - €{token.value}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif cmd == 'list':
            tokens = self.system.token_manager.list_all_tokens()
            if not tokens:
                print("No tokens found")
                return
            
            print(f"\nTokens ({len(tokens)}):")
            for token in tokens:
                print(f"  {token.token_id[:8]}... - €{token.value} (Owner: {token.owner_wallet_id[:8]}...)")
        
        elif cmd == 'info':
            if len(args) < 2:
                print("Usage: token info <token_id>")
                return
            
            token_id = args[1]
            token = self.system.token_manager.get_token(token_id)
            if not token:
                print(f"Token {token_id} not found")
                return
            
            print(f"\nToken Details:")
            print(f"  ID: {token.token_id}")
            print(f"  Value: €{token.value}")
            print(f"  Owner: {token.owner_wallet_id}")
            print(f"  Issued By: {token.issued_by}")
        
        elif cmd == 'balance':
            if len(args) < 2:
                print("Usage: token balance <wallet_id>")
                return
            
            wallet_id = args[1]
            tokens = self.system.token_manager.get_tokens_by_owner(wallet_id)
            total_value = sum(token.value for token in tokens)
            
            print(f"\nToken Balance: €{total_value}")
            for token in tokens:
                print(f"  {token.token_id[:8]}... - €{token.value}")
        
        else:
            print(f"Unknown token command: {cmd}")
    
    def handle_voucher_commands(self, args: List[str]):
        """Handle voucher-related commands"""
        if not args:
            print("❌ Usage: voucher <command> [args]")
            return
        
        cmd = args[0].lower()
        
        if cmd == 'issue':
            if len(args) < 3:
                print("❌ Usage: voucher issue <wallet_id> <limit>")
                return
            
            wallet_id = args[1]
            try:
                limit = int(args[2])
            except ValueError:
                print("❌ Limit must be a number")
                return
            
            try:
                voucher = self.system.voucher_manager.issue_voucher(wallet_id, limit)
                print(f"✅ Issued voucher: {voucher.voucher_id[:8]}... - €{voucher.value_limit} limit")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif cmd == 'list':
            vouchers = self.system.voucher_manager.list_all_vouchers()
            if not vouchers:
                print("📭 No vouchers found")
                return
            
            print(f"\n🎫 Vouchers ({len(vouchers)}):")
            for voucher in vouchers:
                status = "Available" if not voucher.is_used else "Used"
                print(f"  {voucher.voucher_id[:8]}... - €{voucher.value_limit} limit ({status})")
        
        elif cmd == 'info':
            if len(args) < 2:
                print("❌ Usage: voucher info <voucher_id>")
                return
            
            voucher_id = args[1]
            voucher = self.system.voucher_manager.get_voucher(voucher_id)
            if not voucher:
                print(f"❌ Voucher {voucher_id} not found")
                return
            
            print(f"\n🎫 Voucher Details:")
            print(f"  ID: {voucher.voucher_id}")
            print(f"  Value Limit: €{voucher.value_limit}")
            print(f"  Issued To: {voucher.issued_to_wallet_id}")
            print(f"  Status: {'Used' if voucher.is_used else 'Available'}")
            if voucher.is_used:
                print(f"  Used In: {voucher.used_in_transaction}")
        
        elif cmd == 'available':
            if len(args) < 2:
                print("❌ Usage: voucher available <wallet_id>")
                return
            
            wallet_id = args[1]
            vouchers = self.system.voucher_manager.get_available_vouchers_by_wallet(wallet_id)
            
            print(f"\n🎫 Available Vouchers ({len(vouchers)}):")
            for voucher in vouchers:
                print(f"  {voucher.voucher_id[:8]}... - €{voucher.value_limit} limit")
        
        else:
            print(f"❌ Unknown voucher command: {cmd}")
    
    def handle_transfer_commands(self, args: List[str]):
        """Handle transfer-related commands"""
        if not args:
            print("❌ Usage: transfer <command> [args]")
            return
        
        cmd = args[0].lower()
        
        if cmd == 'list':
            transactions = self.system.transaction_engine.list_all_transactions()
            if not transactions:
                print("📭 No transactions found")
                return
            
            print(f"\n💸 Transactions ({len(transactions)}):")
            for tx in transactions:
                status_icon = "✅" if tx.status.value == "completed" else "⏳" if tx.status.value == "pending" else "❌"
                anonymous_icon = "🔒" if tx.is_anonymous else "👁️"
                aml_icon = "🚨" if tx.aml_flagged else ""
                print(f"  {status_icon} {tx.transaction_id[:8]}... - {tx.sender_wallet_id[:8]}... → {tx.receiver_wallet_id[:8]}... {anonymous_icon} {aml_icon}")
        
        elif cmd == 'info':
            if len(args) < 2:
                print("❌ Usage: transfer info <transaction_id>")
                return
            
            tx_id = args[1]
            tx = self.system.transaction_engine.get_transaction(tx_id)
            if not tx:
                print(f"❌ Transaction {tx_id} not found")
                return
            
            print(f"\n💸 Transaction Details:")
            print(f"  ID: {tx.transaction_id}")
            print(f"  From: {tx.sender_wallet_id}")
            print(f"  To: {tx.receiver_wallet_id}")
            print(f"  Token: {tx.token_id}")
            print(f"  Anonymous: {'Yes' if tx.is_anonymous else 'No'}")
            print(f"  Status: {tx.status.value}")
            print(f"  AML Flagged: {'Yes' if tx.aml_flagged else 'No'}")
            if tx.aml_reason:
                print(f"  AML Reason: {tx.aml_reason}")
        
        elif cmd == 'anonymous':
            if len(args) < 5:
                print("❌ Usage: transfer anonymous <sender> <receiver> <token_id> <voucher_id>")
                return
            
            sender_id = args[1]
            receiver_id = args[2]
            token_id = args[3]
            voucher_id = args[4]
            
            try:
                tx = self.system.transaction_engine.execute_transfer(sender_id, receiver_id, token_id, voucher_id)
                print(f"✅ Anonymous transfer completed: {tx.transaction_id[:8]}...")
                if tx.aml_flagged:
                    print(f"🚨 Transaction flagged for AML monitoring")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        else:
            # Regular transfer
            if len(args) < 4:
                print("❌ Usage: transfer <sender> <receiver> <token_id> [voucher_id]")
                return
            
            sender_id = args[0]
            receiver_id = args[1]
            token_id = args[2]
            voucher_id = args[3] if len(args) > 3 else None
            
            try:
                tx = self.system.transaction_engine.execute_transfer(sender_id, receiver_id, token_id, voucher_id)
                print(f"✅ Transfer completed: {tx.transaction_id[:8]}...")
                if tx.aml_flagged:
                    print(f"🚨 Transaction flagged for AML monitoring")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def handle_offline_commands(self, args: List[str]):
        """Handle offline transaction commands"""
        if not args:
            print("❌ Usage: offline <command> [args]")
            return
        
        cmd = args[0].lower()
        
        if cmd == 'create':
            if len(args) < 4:
                print("❌ Usage: offline create <sender> <receiver> <token_id> [voucher_id]")
                return
            
            sender_id = args[1]
            receiver_id = args[2]
            token_id = args[3]
            voucher_id = args[4] if len(args) > 4 else None
            
            try:
                offline_tx = self.system.offline_manager.create_offline_transaction(sender_id, receiver_id, token_id, voucher_id)
                print(f"✅ Offline transaction created: {offline_tx.offline_id[:8]}...")
                print(f"   Status: {offline_tx.status.value}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif cmd == 'sign':
            if len(args) < 4:
                print("❌ Usage: offline sign <offline_id> <wallet_id> <signature>")
                return
            
            offline_id = args[1]
            wallet_id = args[2]
            signature = args[3]
            
            try:
                success = self.system.offline_manager.sign_offline_transaction(offline_id, wallet_id, signature)
                if success:
                    print(f"✅ Transaction signed successfully")
                else:
                    print(f"❌ Failed to sign transaction")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif cmd == 'sync':
            if len(args) < 2:
                print("❌ Usage: offline sync <offline_id>")
                return
            
            offline_id = args[1]
            
            try:
                success = self.system.offline_manager.sync_with_ledger(offline_id)
                if success:
                    print(f"✅ Offline transaction synced with ledger")
                else:
                    print(f"❌ Failed to sync transaction")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif cmd == 'list':
            offline_txs = self.system.offline_manager.list_all_offline_transactions()
            if not offline_txs:
                print("📭 No offline transactions found")
                return
            
            print(f"\n📱 Offline Transactions ({len(offline_txs)}):")
            for tx in offline_txs:
                status_icon = "✅" if tx.status.value == "synced" else "⏳" if tx.status.value == "signed" else "📝"
                print(f"  {status_icon} {tx.offline_id[:8]}... - {tx.sender_wallet_id[:8]}... → {tx.receiver_wallet_id[:8]}... (€{tx.value})")
        
        else:
            print(f"❌ Unknown offline command: {cmd}")
    
    def handle_compliance_commands(self, args: List[str]):
        """Handle compliance-related commands"""
        if not args:
            print("❌ Usage: compliance <command> [args]")
            return
        
        cmd = args[0].lower()
        
        if cmd == 'list':
            aml_entries = self.system.compliance_manager.get_aml_entries()
            if not aml_entries:
                print("📭 No AML entries found")
                return
            
            print(f"\n🚨 AML Entries ({len(aml_entries)}):")
            for entry in aml_entries:
                escalated_icon = "🚨" if entry.escalated else ""
                print(f"  {entry.transaction_id[:8]}... - €{entry.amount} (Risk: {entry.risk_score:.2f}) {escalated_icon}")
        
        elif cmd == 'stats':
            stats = self.system.compliance_manager.get_compliance_statistics()
            print(f"\n📊 Compliance Statistics:")
            print(f"  Total Flagged: {stats['total_flagged_transactions']}")
            print(f"  High Risk: {stats['high_risk_transactions']}")
            print(f"  Escalated: {stats['escalated_transactions']}")
            print(f"  Authority Contacted: {'Yes' if stats['authority_contacted'] else 'No'}")
            print(f"  Average Risk Score: {stats['average_risk_score']:.2f}")
        
        elif cmd == 'export':
            try:
                filename = self.system.compliance_manager.export_aml_report()
                print(f"✅ AML report exported: {filename}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        else:
            print(f"❌ Unknown compliance command: {cmd}")
    
    def handle_ledger_commands(self, args: List[str]):
        """Handle ledger-related commands"""
        if not args:
            print("❌ Usage: ledger <command> [args]")
            return
        
        cmd = args[0].lower()
        
        if cmd == 'list':
            entries = self.system.ledger_manager.list_all_entries()
            if not entries:
                print("📭 No ledger entries found")
                return
            
            print(f"\n📋 Ledger Entries ({len(entries)}):")
            for entry in entries:
                type_icon = "🔒" if entry.entry_type.value == "anonymous" else "👁️"
                print(f"  {type_icon} {entry.entry_id} - €{entry.value} ({entry.entry_type.value})")
        
        elif cmd == 'stats':
            stats = self.system.ledger_manager.get_ledger_statistics()
            print(f"\n📊 Ledger Statistics:")
            print(f"  Total Entries: {stats['total_entries']}")
            print(f"  Anonymous: {stats['anonymous_entries']} ({stats['anonymous_percentage']:.1f}%)")
            print(f"  Non-Anonymous: {stats['non_anonymous_entries']}")
            print(f"  AML Flagged: {stats['aml_flagged_entries']}")
            print(f"  Total Value: €{stats['total_value']}")
            print(f"  Anonymous Value: €{stats['anonymous_value']} ({stats['value_anonymous_percentage']:.1f}%)")
        
        elif cmd == 'export':
            try:
                filename = self.system.ledger_manager.export_aml_loggable_transactions()
                print(f"✅ AML loggable transactions exported: {filename}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        else:
            print(f"❌ Unknown ledger command: {cmd}")
    
    def handle_zkp_commands(self, args: List[str]):
        """Handle ZKP-related commands"""
        if not args:
            print("❌ Usage: zkp <command> [args]")
            return
        
        cmd = args[0].lower()
        
        if cmd == 'range':
            if len(args) < 4:
                print("❌ Usage: zkp range <wallet_id> <min> <max>")
                return
            
            wallet_id = args[1]
            try:
                min_val = int(args[2])
                max_val = int(args[3])
            except ValueError:
                print("❌ Min and max must be numbers")
                return
            
            try:
                proof = self.system.zkp_manager.generate_range_proof(wallet_id, min_val, max_val)
                print(f"✅ Range proof generated: {proof.proof_id[:8]}...")
                print(f"   Range: €{min_val} - €{max_val}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif cmd == 'verify':
            if len(args) < 2:
                print("❌ Usage: zkp verify <proof_id>")
                return
            
            proof_id = args[1]
            proof = self.system.zkp_manager.get_proof(proof_id)
            if not proof:
                print(f"❌ Proof {proof_id} not found")
                return
            
            try:
                if proof.proof_type.value == "range_proof":
                    success = self.system.zkp_manager.verify_range_proof(proof_id)
                elif proof.proof_type.value == "equality_proof":
                    success = self.system.zkp_manager.verify_equality_proof(proof_id)
                elif proof.proof_type.value == "membership_proof":
                    success = self.system.zkp_manager.verify_membership_proof(proof_id)
                else:
                    print(f"❌ Unknown proof type: {proof.proof_type.value}")
                    return
                
                if success:
                    print(f"✅ Proof verified successfully")
                else:
                    print(f"❌ Proof verification failed")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif cmd == 'list':
            proofs = self.system.zkp_manager.list_all_proofs()
            if not proofs:
                print("📭 No ZKP proofs found")
                return
            
            print(f"\n🔐 ZKP Proofs ({len(proofs)}):")
            for proof in proofs:
                verified_icon = "✅" if proof.verified else "⏳"
                print(f"  {verified_icon} {proof.proof_id[:8]}... - {proof.proof_type.value}")
        
        elif cmd == 'stats':
            stats = self.system.zkp_manager.get_zkp_statistics()
            print(f"\n📊 ZKP Statistics:")
            print(f"  Total Proofs: {stats['total_proofs']}")
            print(f"  Verified: {stats['verified_proofs']}")
            print(f"  Unverified: {stats['unverified_proofs']}")
            print(f"  Verification Rate: {stats['verification_rate']:.1f}%")
            print(f"  Proof Types:")
            for proof_type, count in stats['proof_types'].items():
                print(f"    {proof_type}: {count}")
        
        else:
            print(f"❌ Unknown ZKP command: {cmd}")
    
    def handle_export_commands(self, args: List[str]):
        """Handle export commands"""
        if not args:
            print("❌ Usage: export <command> [args]")
            return
        
        cmd = args[0].lower()
        
        if cmd == 'all':
            try:
                files = self.system.export_system_data()
                print(f"✅ System data exported:")
                for file_type, filename in files.items():
                    print(f"   {file_type}: {filename}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif cmd == 'aml':
            try:
                filename = self.system.compliance_manager.export_aml_report()
                print(f"✅ AML report exported: {filename}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif cmd == 'ledger':
            try:
                filename = self.system.ledger_manager.export_aml_loggable_transactions()
                print(f"✅ Ledger data exported: {filename}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif cmd == 'zkp':
            try:
                filename = self.system.zkp_manager.export_zkp_proofs()
                print(f"✅ ZKP proofs exported: {filename}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        else:
            print(f"❌ Unknown export command: {cmd}")
    
    def run_demo(self):
        """Run a comprehensive demonstration"""
        print("\n🎭 Running Privacy Network System Demo...")
        print("=" * 50)
        
        try:
            # Create wallets
            print("1️⃣ Creating wallets...")
            wallet1 = self.system.wallet_manager.create_wallet()
            wallet2 = self.system.wallet_manager.create_wallet()
            wallet3 = self.system.wallet_manager.create_wallet()
            print(f"   ✅ Created 3 wallets")
            
            # Issue tokens
            print("2️⃣ Issuing tokens...")
            token1 = self.system.token_manager.issue_token(50, wallet1.wallet_id)
            token2 = self.system.token_manager.issue_token(100, wallet2.wallet_id)
            token3 = self.system.token_manager.issue_token(25, wallet3.wallet_id)
            print(f"   ✅ Issued tokens: €{token1.value}, €{token2.value}, €{token3.value}")
            
            # Issue vouchers
            print("3️⃣ Issuing anonymity vouchers...")
            voucher1 = self.system.voucher_manager.issue_voucher(wallet1.wallet_id, 50)
            voucher2 = self.system.voucher_manager.issue_voucher(wallet2.wallet_id, 100)
            print(f"   ✅ Issued vouchers with limits: €{voucher1.value_limit}, €{voucher2.value_limit}")
            
            # Regular transfer
            print("4️⃣ Executing regular transfer...")
            tx1 = self.system.transaction_engine.execute_transfer(wallet1.wallet_id, wallet2.wallet_id, token1.token_id)
            print(f"   ✅ Regular transfer completed ({'AML flagged' if tx1.aml_flagged else 'no flags'})")
            
            # Anonymous transfer
            print("5️⃣ Executing anonymous transfer...")
            tx2 = self.system.transaction_engine.execute_transfer(wallet2.wallet_id, wallet3.wallet_id, token2.token_id, voucher2.voucher_id)
            print(f"   ✅ Anonymous transfer completed")
            
            # Offline transfer
            print("6️⃣ Creating offline transfer...")
            offline_tx = self.system.offline_manager.create_offline_transaction(wallet3.wallet_id, wallet1.wallet_id, token3.token_id)
            print(f"   ✅ Offline transfer created")
            
            # ZKP proof
            print("7️⃣ Generating zero-knowledge proof...")
            proof = self.system.zkp_manager.generate_range_proof(wallet1.wallet_id, 0, 200)
            print(f"   ✅ Range proof generated")
            
            # Final status
            print("8️⃣ System Status:")
            self.show_status()
            
            print("✅ Demo completed successfully!")
            
        except Exception as e:
            print(f"❌ Demo failed: {e}") 