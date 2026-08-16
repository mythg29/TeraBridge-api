import json
import logging
import time
from api.redis_client import redis_client

logger = logging.getLogger("terabridge.account_pool")

ACCOUNTS_HASH_KEY = "terabridge:accounts"
ACTIVE_ACCOUNT_KEY = "terabridge:active_account_id"

def get_all_accounts():
    """Fetch all accounts from Upstash Redis."""
    if not redis_client:
        return {}
    try:
        raw_accounts = redis_client.hgetall(ACCOUNTS_HASH_KEY) or {}
        accounts = {}
        for acc_id, raw_val in raw_accounts.items():
            try:
                accounts[acc_id] = json.loads(raw_val)
            except Exception:
                pass
        return accounts
    except Exception as e:
        logger.error("Failed to fetch accounts from Redis: %s", e)
        return {}

def get_next_healthy_account():
    """
    Selects the least recently used healthy account from the pool (Round-Robin),
    sets it as the active account, and returns its credentials.
    """
    if not redis_client:
        return None, None

    try:
        accounts = get_all_accounts()
        healthy_accounts = {
            acc_id: data for acc_id, data in accounts.items()
            if data.get("status", "healthy") == "healthy"
        }

        if not healthy_accounts:
            logger.error("No healthy accounts available in the pool!")
            return None, None

        # Sort by last_used timestamp to round-robin
        sorted_accounts = sorted(healthy_accounts.items(), key=lambda x: x[1].get("last_used", 0))
        selected_id, selected_data = sorted_accounts[0]

        # Update last_used timestamp in Redis to place it at the back of the queue
        selected_data["last_used"] = int(time.time())
        redis_client.hset(ACCOUNTS_HASH_KEY, selected_id, json.dumps(selected_data))
        
        # Store active account ID
        redis_client.set(ACTIVE_ACCOUNT_KEY, selected_id)
        logger.info("Rotated and selected healthy account: %s", selected_id)
        return selected_id, selected_data
    except Exception as e:
        logger.error("Error selecting next healthy account: %s", e)
        return None, None

def mark_account_unhealthy(account_id, reason="unknown"):
    """Mark an account as unhealthy in the Redis pool to prevent reuse."""
    if not redis_client or not account_id:
        return
    
    try:
        accounts = get_all_accounts()
        if account_id in accounts:
            data = accounts[account_id]
            data["status"] = "unhealthy"
            data["unhealthy_reason"] = reason
            data["unhealthy_at"] = int(time.time())
            redis_client.hset(ACCOUNTS_HASH_KEY, account_id, json.dumps(data))
            logger.warning("Account '%s' marked UNHEALTHY. Reason: %s", account_id, reason)
    except Exception as e:
        logger.error("Failed to mark account %s unhealthy: %s", account_id, e)
