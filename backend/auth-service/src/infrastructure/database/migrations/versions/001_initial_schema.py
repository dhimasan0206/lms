"""Initial database schema

Revision ID: 001
Revises: 
Create Date: 2023-10-18

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum types
    user_role = postgresql.ENUM('super_admin', 'organization_admin', 'branch_manager', 'teacher', 'student', 'parent', name='user_role')
    user_role.create(op.get_bind())
    
    user_status = postgresql.ENUM('active', 'inactive', 'pending_verification', 'suspended', 'deleted', name='user_status')
    user_status.create(op.get_bind())
    
    token_type = postgresql.ENUM('access', 'refresh', 'reset_password', 'email_verification', 'api_key', name='token_type')
    token_type.create(op.get_bind())
    
    oauth2_provider = postgresql.ENUM('google', 'facebook', 'github', 'apple', name='oauth2_provider')
    oauth2_provider.create(op.get_bind())
    
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('username', sa.String(), nullable=True, unique=True),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=True),
        sa.Column('roles', postgresql.ARRAY(user_role), nullable=False),
        sa.Column('status', user_status, nullable=False, default='pending_verification'),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('profile_image_url', sa.String(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('email_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('phone_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('preferences', postgresql.JSONB(), nullable=False, server_default='{}'),
        sa.Column('metadata', postgresql.JSONB(), nullable=False, server_default='{}')
    )
    
    # Create indexes on users table
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_username', 'users', ['username'])
    op.create_index('ix_users_organization_id', 'users', ['organization_id'])
    op.create_index('ix_users_branch_id', 'users', ['branch_id'])
    
    # Create tokens table
    op.create_table('tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('token_type', token_type, nullable=False),
        sa.Column('token_value', sa.Text(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('revoked', sa.Boolean(), nullable=False, default=False),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.Column('device_info', postgresql.JSONB(), nullable=False, server_default='{}'),
        sa.Column('metadata', postgresql.JSONB(), nullable=False, server_default='{}'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Create indexes on tokens table
    op.create_index('ix_tokens_user_id', 'tokens', ['user_id'])
    op.create_index('ix_tokens_token_value', 'tokens', ['token_value'])
    op.create_index('ix_tokens_expires_at', 'tokens', ['expires_at'])
    
    # Create oauth2_connections table
    op.create_table('oauth2_connections',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('provider', oauth2_provider, nullable=False),
        sa.Column('provider_user_id', sa.String(), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=True),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('token_expires_at', sa.DateTime(), nullable=True),
        sa.Column('profile_data', postgresql.JSONB(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('provider', 'provider_user_id', name='uq_oauth2_provider_user_id')
    )
    
    # Create indexes on oauth2_connections table
    op.create_index('ix_oauth2_connections_user_id', 'oauth2_connections', ['user_id'])
    op.create_index('ix_oauth2_connections_provider', 'oauth2_connections', ['provider'])
    op.create_index('ix_oauth2_connections_provider_user_id', 'oauth2_connections', ['provider_user_id'])


def downgrade() -> None:
    # Drop tables
    op.drop_table('oauth2_connections')
    op.drop_table('tokens')
    op.drop_table('users')
    
    # Drop enum types
    op.execute('DROP TYPE user_role')
    op.execute('DROP TYPE user_status')
    op.execute('DROP TYPE token_type')
    op.execute('DROP TYPE oauth2_provider') 