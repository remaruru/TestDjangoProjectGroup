from django.shortcuts import redirect

def require_role_selection(backend, strategy, details, response, user=None, *args, **kwargs):
    """
    If a new user logs in via Social Auth, they might not have a saved role (is_customer or is_seller).
    Redirect them to a page to choose their role.
    """
    if user:
        if not user.is_customer and not user.is_seller:
            # We save the user ID in the session temporarily to identify them in the role selection view
            strategy.session_set('partial_pipeline_user_id', user.id)
            return redirect('users:social_role_select')
